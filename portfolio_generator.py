import markdown

def generate_portfolio(student_data: str) -> str:
    md_content = f"""
# Portfolio

## About Me
{student_data}

## Skills & Projects
(Generated dynamically from provided information)

## Contact
Email and LinkedIn details can be added here.
"""

    html = markdown.markdown(md_content)
    return html
