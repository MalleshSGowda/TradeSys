


-- Incremental Load
insert into stage1_db.stg_mutual_fund_list(amc, scheme_code, scheme_name, scheme_type, scheme_category, scheme_nav_name, scheme_minimum_amount, launch_date, closure_date, isin_div_payout_isin_growth_isin_div_reinvestment)
SELECT t1.amc, t1.scheme_code, t1.scheme_name, t1.scheme_type, t1.scheme_category, t1.scheme_nav_name, t1.scheme_minimum_amount,STR_TO_DATE(t1.launch_date,'%d-%b-%Y') as  launch_date, STR_TO_DATE(t1.closure_date,'%d-%b-%Y') as  closure_date, t1.isin_div_payout_isin_growth_isin_div_reinvestment FROM source_db.mutual_fund_list t1 
right join stage1_db.stg_mutual_fund_list t2 on t1.scheme_code = t2.scheme_code
where t2.scheme_code  is null;

-- Incremental Load
insert ignore into stage1_db.stg_mutual_fund_nav_history(date_nav, date_nav_id, nav, scheme_code,scheme_name, isin_growth, isin_div_reinvestment)
select STR_TO_DATE(date_nav, '%Y-%m-%d') as date_nav, date_nav_id, net_asset_value,scheme_code,scheme_name,isin_div_payout_isin_growth,isin_div_reinvestment 
from source_db.mutual_fund_nav_present;


-- Full Load
insert into stage1_db.stg_mutual_fund_list(amc, scheme_code, scheme_name, scheme_type, scheme_category, scheme_nav_name, scheme_minimum_amount, launch_date, closure_date, isin_div_payout_isin_growth_isin_div_reinvestment)
select amc, scheme_code, scheme_name, scheme_type, scheme_category, scheme_nav_name, scheme_minimum_amount,STR_TO_DATE(launch_date, '%d-%b-%Y') as  launch_date, STR_TO_DATE(closure_date, '%d-%b-%Y') as  closure_date, isin_div_payout_isin_growth_isin_div_reinvestment
from source_db.mutual_fund_list;

-- Full load

insert ignore into stage1_db.stg_mutual_fund_nav_history(date_nav, date_nav_id, nav, scheme_code, fund_house, scheme_type, scheme_category, scheme_name, isin_growth, isin_div_reinvestment)
select STR_TO_DATE(date, '%d-%m-%Y') as date,date_nav_id, nav,scheme_code, fund_house, scheme_type, scheme_category,scheme_name, isin_growth, isin_div_reinvestment
from source_db.mutual_fund_nav_history;
 

 -- Migregate query

insert ignore into stage1_db.stg_mutual_fund_nav_history(
date_nav,date_nav_id, nav, scheme_code, fund_house, scheme_type, scheme_category, scheme_name, min_nav, max_nav, Start_date, last_date)
select date_nav,DATE_FORMAT(STR_TO_DATE(date_nav, '%d-%m-%Y'), '%Y%m%d') as date_nav_id, nav, scheme_code, fund_house, scheme_type, scheme_category, scheme_name, min_nav, max_nav, Start_date, last_date
FROM stg_trading_system.stg_mutual_fund_nav_history 
-- where scheme_code > 0 and scheme_code <=104272;