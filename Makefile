PY?=python3.12

run_daily:
	$(PY) -m pipeline.run_daily

backfill:
	$(PY) -m pipeline.backfill --days 30

dbt_docs:
	cd dbt && dbt deps && dbt docs generate && dbt docs serve

clean:
	rm -f warehouse/ecom.duckdb
	rm -rf exports dbt/target raw
