
drop table stage1_db.`stg_mutual_fund_list`;

CREATE TABLE stage1_db.`stg_mutual_fund_list` ( 
  `amc` text,
  `scheme_code` bigint,
  `scheme_name` varchar(750),
  `scheme_type` varchar(750),
  `scheme_category` varchar(750),
  `scheme_nav_name` varchar(1500),
  `scheme_minimum_amount` varchar(750),
  `launch_date` date,
  `closure_date` date,
  `isin_div_payout_isin_growth_isin_div_reinvestment` varchar(1500),
  PRIMARY KEY (scheme_code, scheme_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

drop table stage1_db.`stg_mutual_fund_nav_history`;


CREATE TABLE stage1_db.`stg_mutual_fund_nav_history` (
  `date_nav` date NOT NULL,
  `date_nav_id` bigint NOT NULL,
  `nav` decimal(25,15) NOT NULL,
  `scheme_code` bigint NOT NULL,
  `fund_house` varchar(750) DEFAULT NULL,
  `scheme_type` varchar(750) DEFAULT NULL,
  `scheme_category` varchar(750) DEFAULT NULL,
  `scheme_name` varchar(750) DEFAULT NULL,
  `isin_growth` varchar(750) DEFAULT NULL,
  `isin_div_reinvestment` varchar(750) DEFAULT NULL,
  `min_nav` varchar(250) DEFAULT NULL,
  `max_nav` varchar(250) DEFAULT NULL,
  `Start_date` date DEFAULT NULL,
  `last_date` date DEFAULT NULL,
  PRIMARY KEY (`date_nav`,`nav`,`scheme_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;