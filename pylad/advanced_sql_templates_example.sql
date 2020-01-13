create table db_stg.analytics.transactions (
    transaction_id int,
    user_id int,
    transaction_date date,
    store_id int,
    payment_method varchar(10),
    amount float
)
;

insert into db_stg.analytics.transactions
(transaction_id, user_id, transaction_date, store_id, payment_method, amount)
values
    (1, 1234, '2019-03-02', 1, 'cash', 5.25),
    (1, 1234, '2019-03-01', 1, 'credit', 10.75),
    (1, 1234, '2019-03-02', 2, 'cash', 25.50),
    (1, 1234, '2019-03-03', 2, 'credit', 17.00),
    (1, 4321, '2019-03-01', 2, 'cash', 20.00),
    (1, 4321, '2019-03-02', 2, 'credit', 30.00),
    (1, 4321, '2019-03-03', 1, 'cash', 3.00)
;

select
    store_id
    , payment_method
    , count(*) as num_transactions
    , sum(amount) as total_amount
    , avg(amount) as avg_amount
from
    transactions
group by
    store_id
    , payment_method
order by total_amount desc
;


select
    sum(amount) as total_amount
    , store_id as store_id
    , case when payment_method = 'cash' then 'cash' else 'card' end as card_or_cash
    , count(*) as num_transactions
    , avg(amount) as avg_amount
from
    transactions
group by
    store_id
    , card_or_cash
order by total_amount desc
;

with
user_transactions as (
select
    store_id
    , user_id
    , count(*) as num_transactions
    , min(amount) as min_amount
    , max(amount) as max_amount
    , sum(amount) as total_amount
    , avg(amount) as avg_amount
    , case when max_amount > 15 then 1 else 0 end as is_high_spender
from
    transactions
group by
    store_id
    , user_id
)
,
store_transactions as (
select
    store_id
    , count(*) as user_count
    , sum(num_transactions) as num_transactions
    , sum(total_amount) as total_amount
    , sum(case when is_high_spender > 0 then total_amount else 0.0 end) as high_spender_amount
    , sum(is_high_spender) as high_spender_count
from
    user_transactions
group by store_id
)
select
    num_transactions / user_count as avg_user_num_transactions
    , total_amount / user_count as avg_user_spend
    , high_spender_count / user_count * 100 as pct_high_spenders
    -- division by zero
    --, high_spender_amount / high_spender_count as avg_high_spender_spend
from
    store_transactions
order by total_amount desc
;
