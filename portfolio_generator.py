import markdown

def generate_portfolio(student_data):
    portfolio_md = f"""
# {student_data['name']} – Portfolio

## About Me
{student_data['summary']}

## Skills
{", ".join(student_data['skills'])}

## Projects
"""
    for project in student_data["projects"]:
        portfolio_md += f"""
### {project['title']}
{project['description']}
Technologies: {project['tech']}
"""

    html = markdown.markdown(portfolio_md)
    return html
