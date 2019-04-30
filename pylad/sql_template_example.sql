create table transactions (
    transaction_id int,
    user_id int,
    transaction_date date,
    amount float
)
;

insert into transactions (transaction_id, user_id, transaction_date, amount)
values (1, 1234, '2019-03-02', 5.25);
insert into _transactions (transaction_id, user_id, transaction_date, amount)
values (1, 1234, '2019-03-01', 15.75);
insert into transactions (transaction_id, user_id, transaction_date, amount)
values (1, 1234, '2019-03-02', 25.50);
insert into transactions (transaction_id, user_id, transaction_date, amount)
values (1, 1234, '2019-03-03', 10.00);
insert into transactions (transaction_id, user_id, transaction_date, amount)
values (1, 4321, '2019-03-01', 20.00);
insert into transactions (transaction_id, user_id, transaction_date, amount)
values (1, 4321, '2019-03-02', 30.00);

select
    user_id
    , count(*) as num_transactions
    , sum(amount) as total_amount
from
    transactions
where
    user_id = 1234
    and transaction_date = '2019-03-02'
group by
    user_id
;

-- Result:
-- 1234|2|30.75

