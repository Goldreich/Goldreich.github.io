document.querySelectorAll('[data-interval]').forEach(button=>{
  button.addEventListener('click',()=>{
    const level=button.dataset.interval;
    document.querySelectorAll('[data-interval]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    document.querySelectorAll('[data-chart-row]').forEach(row=>{
      const low=Number(row.dataset['lo'+level]),high=Number(row.dataset['hi'+level]);
      const interval=row.querySelector('.interval');interval.style.left=`${low/40*100}%`;interval.style.width=`${(high-low)/40*100}%`;
      row.setAttribute('aria-label',`${row.dataset.name}: expected seats ${row.dataset.mean}; ${level}% interval ${low} to ${high} seats.`);
    });
    document.querySelectorAll('[data-interval-label]').forEach(el=>el.textContent=`${level}% interval`);
    const live=document.getElementById('chart-announcement');if(live)live.textContent=`Showing ${level}% model uncertainty intervals.`;
  });
});
const sorter=document.getElementById('chart-sort');
if(sorter)sorter.addEventListener('change',()=>{
  const container=document.getElementById('seat-chart-rows');
  [...container.querySelectorAll('[data-chart-row]')].sort((a,b)=>sorter.value==='name'?a.dataset.name.localeCompare(b.dataset.name):Number(b.dataset.mean)-Number(a.dataset.mean)).forEach(r=>container.appendChild(r));
});
