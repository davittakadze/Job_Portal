from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from Form import Form


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'  # for sqlalchemy
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)  # Database formation


# database description
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    descr = db.Column(db.String)
    company = db.Column(db.String)
    category = db.Column(db.String)
    salary = db.Column(db.Float, nullable=True)

    # dict for api
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'descr': self.descr,
            'company': self.company,
            'category': self.category,
            'salary': self.salary
        }


# homepage(all jobs)
@app.route('/')
def get_jobs():
    jobs = [job.to_dict() for job in Job.query.all()]

    return render_template('index.html', jobs=jobs)


# api page
@app.route('/api')
def show_jobs():
    jobs = [job.to_dict() for job in Job.query.all()]
    return jobs


# add, post-> add, get -> for showing inputs
@app.route('/add_job', methods=['POST', 'GET'])
def add_jobs():
    form = Form()
    if form.validate_on_submit():
        name = form.name.data
        descr = form.descr.data
        company = form.company.data
        category = form.category.data
        salary = form.salary.data or None

        db.session.add(Job(name=name, descr=descr, company=company, category=category, salary=salary))
        db.session.commit()
        return "Jobs finally added"
    return render_template('add_job.html', form=form)


@app.route('/category/<string:category>')
def show_category(category):
    jobs = [job.to_dict() for job in Job.query.filter(Job.category == category)]
    return jobs


@app.route('/company/<string:company>')
def show_company(company):
    jobs = [job.to_dict() for job in Job.query.filter(Job.company == company)]
    return jobs


@app.route('/delete/<int:id>')
def delete_job(id):
    job = Job.query.get(id)
    db.session.delete(job)
    db.session.commit()
    return "Successfully delete", 200


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update_jobs(id):
    job = Job.query.get(id)
    form = Form()
    if form.validate_on_submit():
        job.name = form.name.data
        job.descr = form.descr.data
        job.company = form.company.data
        job.category = form.category.data
        job.salary = form.salary.data
        db.session.commit()
        return 'Finally updated'
    return render_template('update.html', form=form)


@app.route('/job/<int:id>')
def get_info(id):
    job = Job.query.get(id)
    return render_template('job.html', job=job)


@app.route('/<int:id>')
def get_current_job_id():
    job_id = request.args.get('id')
    return job_id


@app.route('/search')
def search():
    jobs = [job.to_dict() for job in Job.query.all()]
    keyword = request.args.get('keyword', '')
    filtered_jobs = [job for job in jobs if keyword.lower() in job['name'].lower()]
    return render_template('index.html', jobs=filtered_jobs)


@app.route('/')
def index():
    job_id = get_current_job_id()

    return render_template('index.html', job_id=job_id)


with app.app_context():
    db.create_all()
    """app.run()"""
