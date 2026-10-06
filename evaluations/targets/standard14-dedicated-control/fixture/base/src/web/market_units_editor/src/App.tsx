import {useState} from 'react';
export type Fund = {name:string; asset_class:string; currency:string; units:string; source_symbol:string; csv_url:string; audit_match_key?:string};
export default function App({funds = [], search = ''}: {funds?: Fund[]; search?: string}) {
  const [query, setQuery] = useState(search);
  const rows = funds.filter(f => f.name.includes(query));
  const hasAuditKey = funds.some(f => (f.audit_match_key ?? '').trim() !== '');
  return <><input value={query} onChange={e => setQuery(e.target.value)} /><table><thead><tr>
    <th>Name</th><th>Class</th><th>Currency</th><th>Units</th><th>Symbol</th><th>CSV</th>{hasAuditKey && <th>Audit Key</th>}
  </tr></thead><tbody>{rows.map((f, i) => <tr key={i}>
    <td>{f.name}</td><td>{f.asset_class}</td><td>{f.currency}</td><td>{f.units}</td><td>{f.source_symbol}</td><td>{f.csv_url}</td>{hasAuditKey && <td>{f.audit_match_key}</td>}
  </tr>)}{rows.length === 0 && <tr><td colSpan={hasAuditKey ? 7 : 6}>No records</td></tr>}</tbody></table></>;
}
