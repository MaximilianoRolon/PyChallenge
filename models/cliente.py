from sqlalchemy import Table, Column, Integer, String
from config.db import meta, engine

cliente = Table("cliente", meta,
                Column("id", Integer, primary_key=True),
                Column("nombre", String(255)))

meta.create_all(engine)
