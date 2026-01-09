#!/usr/bin/env python3
"""
pst-timestamp Benchmark Visualizations
Heavily stylized dark theme charts for Twitter
"""

import plotly.graph_objects as go
import numpy as np

# Benchmark data
data = {
    'language': ['C++', 'Go', 'Rust', 'Bash', 'Bun', 'Python', 'Node.js'],
    'time_ms': [1.6, 2.2, 3.1, 6.7, 17.3, 30.0, 37.7],
    'size_bytes': [36_864, 2_411_724, 458_752, 175, 603, 180, 568],
    'loc': [16, 14, 50, 5, 18, 6, 18],
}

# Color palette - neon cyberpunk
colors = {
    'bg': '#0d1117',
    'bg_secondary': '#161b22',
    'grid': '#21262d',
    'text': '#c9d1d9',
    'text_muted': '#8b949e',
    'accent_green': '#00ff88',
    'accent_cyan': '#00d4ff',
    'accent_purple': '#a855f7',
    'accent_pink': '#ff006e',
    'accent_orange': '#ff9500',
    'accent_red': '#ff4444',
    'accent_yellow': '#ffd700'
}

# Language brand colors (high contrast, accessible)
lang_colors = {
    'C++': '#6495ED',    # Cornflower blue
    'Go': '#00ADD8',     # Official Go cyan
    'Rust': '#CE422B',   # Official Rust orange
    'Bash': '#4EAA25',   # Terminal/GNU green
    'Bun': '#F472B6',    # Pink (Bun's vibe)
    'Python': '#FFD43B', # Python yellow
    'Node.js': '#68A063' # Node.js green
}

# ============================================================================
# CHART 1: Speed Comparison (Horizontal Bar Chart)
# ============================================================================

fig1 = go.Figure()

# Sort by speed (fastest first)
sorted_indices = np.argsort(data['time_ms'])
languages = [data['language'][i] for i in sorted_indices]
times = [data['time_ms'][i] for i in sorted_indices]
bar_cols = [lang_colors[lang] for lang in languages]

# Build combined labels: "37.7ms (24x)" for non-baseline, "1.6ms" for C++
text_labels = []
for t in times:
    speedup = t / 1.6
    if speedup == 1.0:
        text_labels.append(f'{t}ms')  # C++ baseline
    else:
        text_labels.append(f'{t}ms ({speedup:.0f}x)')

# Add bars
fig1.add_trace(go.Bar(
    y=languages,
    x=times,
    orientation='h',
    marker=dict(
        color=bar_cols,
        line=dict(color='rgba(255,255,255,0.3)', width=1)
    ),
    text=text_labels,
    textposition='outside',
    textfont=dict(color=colors['text'], size=14, family='Courier New, monospace'),
    hovertemplate='<b>%{y}</b><br>%{x}ms<extra></extra>'
))

fig1.update_layout(
    title=dict(
        text='<b>Execution Time by Language</b><br><span style="color:#8b949e;font-size:14px">Same script, 7 languages, 500 runs each (hyperfine)</span>',
        font=dict(size=24, color=colors['text']),
        x=0.5,
        xanchor='center'
    ),
    paper_bgcolor=colors['bg'],
    plot_bgcolor=colors['bg'],
    font=dict(color=colors['text']),
    xaxis=dict(
        title=dict(text='Execution Time (ms)', font=dict(size=14, color=colors['text_muted'])),
        gridcolor=colors['grid'],
        gridwidth=1,
        zeroline=False,
        range=[0, 55]
    ),
    yaxis=dict(
        gridcolor='rgba(0,0,0,0)',
        categoryorder='array',
        categoryarray=languages
    ),
    margin=dict(l=100, r=120, t=100, b=60),
    height=500,
    width=900,
    showlegend=False
)

# Add trophy to winner
fig1.add_annotation(x=-0.5, y='C++', text='🥇', showarrow=False, font=dict(size=20), xanchor='right')

fig1.write_html('results/speed_comparison.html', include_plotlyjs='cdn')
fig1.write_image('results/speed_comparison.png', scale=2)
print("✓ Created speed_comparison.html and .png")


# ============================================================================
# CHART 2: Size vs Speed Scatter (Log Scale)
# ============================================================================

fig2 = go.Figure()

# Uses lang_colors defined at top (brand colors)

# Add scatter points with glow effect
for lang, time, size, loc in zip(data['language'], data['time_ms'], data['size_bytes'], data['loc']):
    # Glow layer
    fig2.add_trace(go.Scatter(
        x=[size], y=[time],
        mode='markers',
        marker=dict(size=loc * 2 + 30, color=lang_colors[lang], opacity=0.2),
        hoverinfo='skip', showlegend=False
    ))
    
    # Main point
    fig2.add_trace(go.Scatter(
        x=[size], y=[time],
        mode='markers+text',
        marker=dict(size=loc * 1.5 + 15, color=lang_colors[lang], line=dict(color='white', width=2), opacity=0.9),
        text=lang,
        textposition='top center',
        textfont=dict(color=colors['text'], size=12, family='Courier New'),
        name=lang,
        hovertemplate=f'<b>{lang}</b><br>Time: {time}ms<br>Size: {size:,} bytes<br>LOC: {loc}<extra></extra>'
    ))

fig2.update_layout(
    title=dict(
        text='<b>The Tradeoff: Speed vs Binary Size</b><br><span style="color:#8b949e;font-size:14px">Bubble size = lines of code</span>',
        font=dict(size=24, color=colors['text']),
        x=0.5,
        xanchor='center'
    ),
    paper_bgcolor=colors['bg'],
    plot_bgcolor=colors['bg_secondary'],
    font=dict(color=colors['text']),
    xaxis=dict(
        title=dict(text='Binary/Script Size', font=dict(size=14, color=colors['text_muted'])),
        type='log',
        gridcolor=colors['grid'],
        gridwidth=1,
        zeroline=False,
        tickvals=[100, 1000, 10_000, 100_000, 1_000_000, 10_000_000],
        ticktext=['100B', '1KB', '10KB', '100KB', '1MB', '10MB'],
        range=[1.7, 7.5]  # log10(50) to log10(10M)
    ),
    yaxis=dict(
        title=dict(text='Execution Time (ms)', font=dict(size=14, color=colors['text_muted'])),
        gridcolor=colors['grid'],
        gridwidth=1,
        zeroline=False,
        range=[-3, 45]
    ),
    margin=dict(l=80, r=40, t=100, b=80),
    height=600,
    width=900,
    showlegend=False
)

fig2.write_html('results/size_vs_speed.html', include_plotlyjs='cdn')
fig2.write_image('results/size_vs_speed.png', scale=2)
print("✓ Created size_vs_speed.html and .png")

print("\n📊 Visualizations complete!")
print("   → results/speed_comparison.html")
print("   → results/speed_comparison.png")
print("   → results/size_vs_speed.html")
print("   → results/size_vs_speed.png")
