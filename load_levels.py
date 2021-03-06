from sqlalchemy import create_engine, Table, MetaData, Column, String
import pandas as pd

DATABASE_URI = "sqlite:///levels_fyi.db"

engine = create_engine(
    DATABASE_URI,
    connect_args={"check_same_thread": False}
)

positions_df = pd.read_sql_query("""
select c.name company_name,
    p.name position,
    level ladder_level,
case instr(salary, 'k')
when 0 then cast(replace(replace(salary, '$', ''), 'm', '') as decimal) * 1000
else cast(replace(replace(salary, '$', ''), 'k', '') as decimal)
end salary
from position p
inner join salary s on p.id = s.position
inner join company c on p.company = c.id
order by 4 desc
""", engine)

benefits_df = pd.read_sql_query("""
select c.name company_name, b.name benefit
from benefit b
inner join company c on b.company = c.id
""", engine)

def classify_position(position: str):
    lower_position = position.lower().strip()
    if 'software' in lower_position and 'manager' in lower_position:
        return 'Software Manager'

    if lower_position == 'program manager':
        return 'Software Manager'

    if 'product' in lower_position and 'manager' in lower_position:
        return 'Product Manager'

    if 'banker' in lower_position or 'accountant' in lower_position or 'finance' in lower_position:
        return 'Financing'

    if lower_position in ['recruiter'] or 'human' in lower_position:
        return 'Human Resources'

    if lower_position in ['civil engineer', 'mechanical engineer', 'biomedical engineer']:
        return 'Others'

    if lower_position in ['software engineer', 'systems engineer']:
        return 'Software Engineer'

    if lower_position == 'applied scientist':
        return 'Data Scientist'

    if lower_position == 'marketing operations':
        return 'Marketing'

    if lower_position == 'security':
        return 'Security Engineer'

    if lower_position == 'business development':
        return 'Business Analyst'

    return position.strip()
