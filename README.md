# Master
We hereby present the source code used to evaluate TPC-H Query 06. (Paper submitted to DATE 2018)HIPE: HMC instruction predication extension applied on database processing

###TPC-H db-generator
- https://github.com/eyalroz/tpch-dbgen

TPC-H Query 06
## Formatted
```sql
SELECT
    sum(l_extendedprice * l_discount) as revenue
FROM
    lineitem
WHERE
    l_shipdate >= date '1994-01-01'
    AND l_shipdate < date '1994-01-01' + interval '1' year
    AND l_discount between 0.06 - 0.01 AND 0.06 + 0.01
    AND l_quantity < 24;
```

## As a one-liner:
```sql
select sum(l_extendedprice * l_discount) as revenue from lineitem where l_shipdate >= date '1994-01-01' and l_shipdate < date '1994-01-01' + interval '1' year and l_discount between 0.06 - 0.01 AND 0.06 + 0.01 and l_quantity < 24;
```
