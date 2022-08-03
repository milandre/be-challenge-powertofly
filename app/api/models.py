from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy_utils import Timestamp

db = SQLAlchemy()


class User(db.Model, Timestamp):
    """User model

    Fields:
        id (int): User model primary key.
        email (str): User email, unique and indexed.
        first_name (str): User first name.
        last_name (str): User last name.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @staticmethod
    def add_fake_users_to_db(buffer, fake):
        print("Starting Bulk...")
        stmt = insert(User).values(buffer)
        stmt = stmt.on_conflict_do_update(
            index_elements=[User.email], set_=dict(first_name=fake.first_name(), last_name=fake.last_name())
        ).returning(User)
        orm_smt = select(User).from_statement(stmt).execution_options(populate_existing=True)
        for user in db.session.execute(orm_smt).scalars():
            print(f'Inserted or updated: {user}')

    @staticmethod
    def generate_fake_users(count=10, max_rows_per_transaction=500000, **kwargs):
        """Generate a number of fake users."""
        from faker import Faker

        fake = Faker()

        buffer = []
        for _ in range(count):
            buffer.append(
                dict(
                    email=fake.unique.email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    created=fake.date_time(),
                )
            )
            if len(buffer) % max_rows_per_transaction == 0:
                User.add_fake_users_to_db(buffer, fake)
                buffer = []

        if len(buffer) > 0:
            User.add_fake_users_to_db(buffer, fake)

    def __repr__(self):
        return '<User \'%s\'>' % self.full_name()
