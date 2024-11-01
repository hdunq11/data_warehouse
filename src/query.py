from src.query_data.c1_rev_by_agecus import c1_rev_by_agecus
from src.query_data.c2_rev_by_typefilm import c2_rev_by_typefilm
from src.query_data.c3_rev_by_gender import c3_rev_by_gender
from src.query_data.c4_rev_by_job import c4_rev_by_job
from src.query_data.c5_rev_by_film import c5_rev_by_film
from src.query_data.c6_rev_by_release_year import c6_rev_by_release_year
from src.query_data.c7_rev_by_duration import c7_rev_by_duration

if __name__ == "__main__":
    c1_rev_by_agecus()
    c2_rev_by_typefilm()
    c3_rev_by_gender()
    c4_rev_by_job()
    c5_rev_by_film()
    c6_rev_by_release_year()
    c7_rev_by_duration()