"""
Data Seeder for Default Job Roles and Keywords
"""

from app import db
from app.models import JobRole

def seed_default_roles():
    """Seed database with default job roles and keywords"""
    
    default_roles = [
        {
            'name': 'Software Engineer',
            'keywords': [
                'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'git',
                'agile', 'scrum', 'api', 'database', 'testing', 'debugging',
                'algorithms', 'data structures', 'object-oriented programming',
                'web development', 'mobile development', 'cloud computing'
            ],
            'description': 'Software development and engineering roles'
        },
        {
            'name': 'Data Scientist',
            'keywords': [
                'python', 'r', 'machine learning', 'deep learning', 'tensorflow',
                'pytorch', 'pandas', 'numpy', 'scikit-learn', 'sql', 'statistics',
                'data analysis', 'data visualization', 'jupyter', 'matplotlib',
                'seaborn', 'big data', 'hadoop', 'spark', 'aws', 'azure'
            ],
            'description': 'Data science and machine learning roles'
        },
        {
            'name': 'Product Manager',
            'keywords': [
                'product management', 'roadmap', 'strategy', 'stakeholder management',
                'user research', 'market analysis', 'agile', 'scrum', 'jira',
                'analytics', 'kpi', 'user experience', 'product development',
                'competitive analysis', 'go-to-market', 'pricing', 'metrics'
            ],
            'description': 'Product management and strategy roles'
        },
        {
            'name': 'Marketing Manager',
            'keywords': [
                'digital marketing', 'content marketing', 'social media', 'seo',
                'sem', 'google analytics', 'campaign management', 'brand management',
                'market research', 'lead generation', 'email marketing',
                'marketing automation', 'crm', 'roi', 'conversion optimization',
                'a/b testing', 'marketing strategy', 'budget management'
            ],
            'description': 'Marketing and digital marketing roles'
        },
        {
            'name': 'Business Analyst',
            'keywords': [
                'business analysis', 'requirements gathering', 'process improvement',
                'stakeholder management', 'documentation', 'sql', 'excel',
                'data analysis', 'reporting', 'project management', 'agile',
                'business intelligence', 'kpi', 'metrics', 'workflow analysis',
                'gap analysis', 'user stories', 'acceptance criteria'
            ],
            'description': 'Business analysis and process improvement roles'
        },
        {
            'name': 'DevOps Engineer',
            'keywords': [
                'devops', 'ci/cd', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
                'terraform', 'ansible', 'jenkins', 'git', 'linux', 'bash',
                'monitoring', 'logging', 'infrastructure', 'automation',
                'cloud computing', 'microservices', 'containerization'
            ],
            'description': 'DevOps and infrastructure roles'
        },
        {
            'name': 'UX/UI Designer',
            'keywords': [
                'user experience', 'user interface', 'wireframing', 'prototyping',
                'figma', 'sketch', 'adobe creative suite', 'user research',
                'usability testing', 'information architecture', 'interaction design',
                'visual design', 'design systems', 'responsive design',
                'accessibility', 'user journey', 'personas', 'design thinking'
            ],
            'description': 'User experience and interface design roles'
        },
        {
            'name': 'Sales Representative',
            'keywords': [
                'sales', 'lead generation', 'prospecting', 'cold calling',
                'relationship building', 'negotiation', 'closing', 'crm',
                'salesforce', 'quota attainment', 'pipeline management',
                'account management', 'customer acquisition', 'revenue growth',
                'sales strategy', 'market penetration', 'consultative selling'
            ],
            'description': 'Sales and business development roles'
        }
    ]
    
    for role_data in default_roles:
        existing_role = JobRole.query.filter_by(name=role_data['name']).first()
        if not existing_role:
            role = JobRole(
                name=role_data['name'],
                description=role_data['description']
            )
            role.set_keywords(role_data['keywords'])
            db.session.add(role)
    
    try:
        db.session.commit()
        print("✅ Default job roles seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding default roles: {str(e)}")
