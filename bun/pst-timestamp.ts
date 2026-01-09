const now = new Date();
const options: Intl.DateTimeFormatOptions = {
  timeZone: 'America/Los_Angeles',
  month: '2-digit',
  day: '2-digit',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
  hour12: true,
  timeZoneName: 'short'
};

const parts = new Intl.DateTimeFormat('en-US', options).formatToParts(now);
const get = (type: string) => parts.find(p => p.type === type)?.value || '';

// Format: MM/DD/YYYY HH:MM AM/PM PST
const formatted = `${get('month')}/${get('day')}/${get('year')} ${get('hour')}:${get('minute')} ${get('dayPeriod')} ${get('timeZoneName')}`;
console.log(formatted);
