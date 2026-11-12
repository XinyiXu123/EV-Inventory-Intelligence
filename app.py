"""EV Inventory Intelligence — reproducible demo using synthetic course data."""
from pathlib import Path
import math
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).parent
st.set_page_config(page_title="EV Inventory Intelligence", page_icon="⚡", layout="wide")

@st.cache_data
def load_data():
    parts = pd.read_csv(ROOT / 'data/parts.csv')
    demand = pd.read_csv(ROOT / 'data/demand.csv', parse_dates=['week_start'])
    inventory = pd.read_csv(ROOT / 'data/inventory.csv', parse_dates=['week_start'])
    original_reorders = pd.read_csv(ROOT / 'data/reorder_recommendations.csv')
    df = demand.merge(inventory, on=['week_start','part_id'], validate='one_to_one').merge(parts,on='part_id',validate='many_to_one')
    df['available_inventory'] = df.stock_on_hand + df.replenishment
    df['units_fulfilled'] = np.minimum(df.available_inventory, df.units_demanded)
    df['unmet_demand'] = (df.units_demanded-df.available_inventory).clip(lower=0)
    df['ending_stock'] = (df.available_inventory-df.units_demanded).clip(lower=0)
    df['holding_cost'] = df.ending_stock*df.holding_cost_per_unit_week
    df['stockout_cost'] = df.unmet_demand*df.stockout_cost_per_unit
    return parts, df, original_reorders

def forecast(history, method):
    values = list(map(float, history))
    if not values: return 0.0
    if method == 'Naive': return values[-1]
    if method == 'Moving average (4 weeks)': return float(np.mean(values[-4:]))
    level = values[0]
    for val in values[1:]: level = .3*val+.7*level
    return float(level)

def rolling_predictions(values, method, test_weeks=12):
    return np.array([max(0, round(forecast(values[:i], method))) for i in range(len(values)-test_weeks,len(values))])

parts, df, original_reorders = load_data()
methods = ['Naive', 'Moving average (4 weeks)', 'Exponential smoothing (α=0.3)']
st.title('⚡ EV Inventory Intelligence')
st.caption('Interactive demand forecasting & replenishment decision support · Academic case study · Synthetic dataset')
st.info('**Demo data:** This is an educational project, not a live inventory system. Historical KPIs are calculated from the supplied weekly data. Simulations are illustrative, not production ordering advice.', icon='ℹ️')

tab1, tab2, tab3, tab4 = st.tabs(['Executive overview','Demand forecasting','Inventory simulator','Recommendations'])
with tab1:
    total_demand = int(df.units_demanded.sum())
    total_unmet = int(df.unmet_demand.sum())
    total_holding = float(df.holding_cost.sum())
    total_stockout = float(df.stockout_cost.sum())
    a,b,c,d = st.columns(4)
    a.metric('Demand (units)',f'{total_demand:,}')
    b.metric('Fill rate',f'{100*(1-total_unmet/total_demand):.1f}%')
    c.metric('Inventory-related cost',f'€{total_holding+total_stockout:,.0f}')
    d.metric('Stockout cost',f'€{total_stockout:,.0f}')
    weekly = df.groupby('week_start',as_index=False)['units_demanded'].sum()
    st.plotly_chart(px.line(weekly,x='week_start',y='units_demanded',title='Total weekly spare-parts demand',labels={'units_demanded':'Units demanded','week_start':'Week'}),use_container_width=True)
    cat = df.groupby('category',as_index=False)[['holding_cost','stockout_cost']].sum().melt(id_vars='category',var_name='Cost type',value_name='EUR')
    st.plotly_chart(px.bar(cat,x='category',y='EUR',color='Cost type',barmode='group',title='Inventory costs by category'),use_container_width=True)
    st.caption('Historical cost = ending-stock holding cost + unmet-demand stockout cost; based on the course assignment assumptions.')

with tab2:
    names = parts.sort_values('part_name').set_index('part_name')['part_id'].to_dict()
    name = st.selectbox('Select spare part',list(names),index=list(names).index('Battery Module A'))
    pid = names[name]
    method = st.selectbox('Forecast method',methods,index=2)
    series = df.loc[df.part_id==pid].sort_values('week_start')
    values = series.units_demanded.to_numpy()
    test = 12
    actual = values[-test:]
    pred = rolling_predictions(values,method,test)
    error = actual-pred
    mae = float(np.abs(error).mean()); mse=float((error**2).mean())
    nonzero = actual!=0
    mape = float(np.mean(np.abs(error[nonzero]/actual[nonzero]))*100) if nonzero.any() else float('nan')
    p = parts.loc[parts.part_id==pid].iloc[0]
    over = float(np.maximum(pred-actual,0).sum()*p.holding_cost_per_unit_week)
    under = float(np.maximum(actual-pred,0).sum()*p.stockout_cost_per_unit)
    x,y,z,w=st.columns(4)
    x.metric('MAE',f'{mae:.2f} units');y.metric('MSE',f'{mse:.2f}');z.metric('MAPE',f'{mape:.1f}%' if np.isfinite(mape) else 'N/A');w.metric('Forecast cost',f'€{over+under:,.0f}')
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=series.week_start,y=values,name='Actual demand',mode='lines+markers'))
    fig.add_trace(go.Scatter(x=series.week_start.iloc[-test:],y=pred,name=f'{method} · rolling 1-week forecast',mode='lines+markers'))
    fig.update_layout(title=f'{name}: historical demand and last {test} test-week forecasts',xaxis_title='Week',yaxis_title='Units')
    st.plotly_chart(fig,use_container_width=True)
    comparison=[]
    for m in methods:
        f=rolling_predictions(values,m,test)
        comparison.append({'Method':m,'MAE':round(float(np.abs(actual-f).mean()),2),'Overage cost (€)':round(float(np.maximum(f-actual,0).sum()*p.holding_cost_per_unit_week),2),'Underage cost (€)':round(float(np.maximum(actual-f,0).sum()*p.stockout_cost_per_unit),2)})
    comp=pd.DataFrame(comparison)
    comp['Total cost (€)']=comp['Overage cost (€)']+comp['Underage cost (€)']
    st.subheader('Compare methods for this part')
    st.dataframe(comp,hide_index=True,use_container_width=True)
    st.caption('Each test-week forecast uses only earlier observed weeks. Forecasts are rounded to nonnegative whole units. Cost assumes one week of holding for overforecast units and lost sales for underforecast units.')

with tab3:
    st.subheader('What-if replenishment simulator')
    sim_name=st.selectbox('Spare part',list(names),index=list(names).index('Battery Cooling Plate'),key='simpart')
    sim_id=names[sim_name]
    p=parts.loc[parts.part_id==sim_id].iloc[0]
    s=df.loc[df.part_id==sim_id].sort_values('week_start')
    baseline=original_reorders.loc[original_reorders.part_id==sim_id].iloc[0]
    col1,col2,col3=st.columns(3)
    stock=col1.number_input('Current stock (units)',min_value=0,max_value=100000,value=int(baseline.current_stock),step=1)
    lead=col2.number_input('Supplier lead time (days)',min_value=1,max_value=365,value=int(p.lead_time_days),step=1)
    service=col3.slider('Target service level (approx.)',min_value=80,max_value=99,value=95,step=1)
    z_values={80:.842,85:1.036,90:1.282,95:1.645,97:1.881,98:2.054,99:2.326}
    z=float(np.interp(service,list(z_values),list(z_values.values())))
    expected=max(0,int(round(forecast(s.units_demanded,'Exponential smoothing (α=0.3)'))))
    lead_weeks=lead/7
    sigma=float(s.units_demanded.std(ddof=1))
    safety=math.ceil(z*sigma*math.sqrt(lead_weeks))
    reorder_point=math.ceil(expected*lead_weeks)+safety
    target=reorder_point+expected
    order=max(0,target-stock) if stock<=reorder_point else 0
    c1,c2,c3,c4=st.columns(4)
    c1.metric('Forecast weekly demand',f'{expected} units')
    c2.metric('Safety stock',f'{safety} units')
    c3.metric('Reorder point',f'{reorder_point} units')
    c4.metric('Suggested order',f'{order} units')
    if stock<=reorder_point: st.warning(f'Stock is at/below the reorder point. Illustrative replenishment quantity: {order} units.')
    else: st.success('Stock is above the reorder point. No immediate order indicated by this rule.')
    st.caption('Safety stock = ceil(z × historical weekly-demand standard deviation × √(lead time in weeks)). The 95% baseline uses z≈1.65. Order-up-to target = reorder point + one week of forecast demand. This is a simplified what-if model; the original CSV is a historical snapshot and is not changed by these controls.')

with tab4:
    st.subheader('Historical reorder recommendations')
    opts=['All']+sorted(original_reorders.category.unique().tolist())
    category=st.selectbox('Filter category',opts)
    subset=original_reorders if category=='All' else original_reorders.loc[original_reorders.category==category]
    st.dataframe(subset,use_container_width=True,hide_index=True)
    st.download_button('Download filtered recommendations CSV',data=subset.to_csv(index=False).encode('utf-8'),file_name='reorder_recommendations_filtered.csv',mime='text/csv')
    st.caption('Recommendations are from the supplied project output (last observed week: 2025-06-23), not live inventory.')

st.divider()
st.caption('Built with Python · Pandas · Plotly · Streamlit | Course dataset is synthetic. See repository README for assumptions, provenance, and individual contributions.')
