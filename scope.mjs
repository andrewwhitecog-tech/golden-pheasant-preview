export function buildScope(input) {
  const errors = {};
  const positive = (key, max = 10000) => { const n = Number(input[key]); if (!String(input[key] ?? '').trim() || !Number.isFinite(n) || n <= 0 || n > max) errors[key] = 'Enter a number greater than 0 and no more than ' + max.toLocaleString() + '.'; return n; };
  if (!['cleaning','painting','mural'].includes(input.kind)) errors.kind = 'Choose a project type.';
  const width = positive('width',1000), height = positive('height',1000), count = positive('count',100);
  if (Number.isFinite(count) && !Number.isInteger(count)) errors.count = 'Use a whole number of surfaces.';
  const openings = Number(input.openings || 0);
  if (!Number.isFinite(openings) || openings < 0) errors.openings = 'Enter 0 or a positive area.';
  const gross = width * height * count;
  if (!errors.width && !errors.height && !errors.count && Number.isFinite(openings) && openings >= gross) errors.openings = 'Excluded area must be smaller than the total surface area.';
  const yearText = String(input.year || '').trim(), year = Number(yearText);
  if (yearText && (!Number.isInteger(year) || year < 1000 || year > new Date().getFullYear()+1)) errors.year = 'Enter a four-digit construction year, or leave it blank.';
  if (!['no','yes','unknown'].includes(input.repair)) errors.repair = 'Choose whether repair is needed.';
  if (Object.keys(errors).length) return {ok:false,errors};
  const area = Number((gross-openings).toPrecision(12));
  const flags = [];
  if (input.kind !== 'cleaning') flags.push('Planning only: painting and mural installation are not open for booking in this preview.');
  if (input.repair !== 'no') flags.push('Scope review needed: repair, coating, sealing or surface disturbance cannot be treated as cleaning-only work.');
  if (yearText && year < 1978) flags.push('Older-property review: confirm coating and material hazards with a qualified professional before disturbing surfaces.');
  if (!yearText) flags.push('Construction year is unknown; confirm it before any surface-disturbing work.');
  const title = {cleaning:'Cleaning-only scope',painting:'Painting planning study',mural:'Mural concept study'}[input.kind];
  const summary = [title, 'Measured surface area: '+area.toLocaleString('en-US',{maximumSignificantDigits:12})+' sq ft', 'Assumptions: '+count+' rectangular surface(s), each '+width+' × '+height+' ft; '+openings+' sq ft excluded.', 'Repair needed: '+input.repair+'. Construction year: '+(yearText||'unknown')+'.', ...flags, 'Measure each surface separately when dimensions differ. Area is approximate and excludes hidden conditions. No price, bid, booking or service acceptance is created.', 'This summary stays on your device unless you choose to share it.'].join(String.fromCharCode(10,10));
  return {ok:true,area,title,flags,summary};
}
