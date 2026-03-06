"""
Generate mock SHL assessment data for testing
Use this if scraping is blocked or for development/testing
"""

import pandas as pd
import random

# Real SHL assessment categories and examples
ASSESSMENTS_DATA = [
    # Programming & Technical Skills
    ("Python New", "Python programming test covering syntax, data structures, and algorithms", "Knowledge & Skills", 11),
    ("Java", "Java programming assessment for object-oriented programming skills", "Knowledge & Skills", 15),
    ("JavaScript", "JavaScript coding test for web development", "Knowledge & Skills", 12),
    ("C++", "C++ programming assessment", "Knowledge & Skills", 15),
    ("SQL", "SQL database query and management test", "Knowledge & Skills", 10),
    ("C#", "C# programming assessment for .NET development", "Knowledge & Skills", 15),
    ("PHP", "PHP web development assessment", "Knowledge & Skills", 12),
    ("Ruby", "Ruby programming test", "Knowledge & Skills", 12),
    ("Swift", "Swift programming for iOS development", "Knowledge & Skills", 12),
    ("Kotlin", "Kotlin programming assessment", "Knowledge & Skills", 12),
    ("TypeScript", "TypeScript programming test", "Knowledge & Skills", 12),
    ("Go", "Go programming language assessment", "Knowledge & Skills", 12),
    ("Rust", "Rust programming test", "Knowledge & Skills", 15),
    ("Scala", "Scala programming assessment", "Knowledge & Skills", 15),
    ("R Programming", "R programming for data analysis", "Knowledge & Skills", 12),
    
    # Data & Analytics
    ("Data Analysis", "Data analysis and interpretation skills", "Knowledge & Skills", 20),
    ("Statistics", "Statistical analysis and methods", "Knowledge & Skills", 25),
    ("Machine Learning", "Machine learning concepts and applications", "Knowledge & Skills", 30),
    ("Data Visualization", "Data visualization and reporting", "Knowledge & Skills", 15),
    ("Excel Advanced", "Advanced Excel skills including formulas and pivot tables", "Knowledge & Skills", 20),
    ("Power BI", "Power BI data visualization and analytics", "Knowledge & Skills", 18),
    ("Tableau", "Tableau data visualization assessment", "Knowledge & Skills", 18),
    ("Big Data", "Big data concepts and technologies", "Knowledge & Skills", 25),
    
    # Cognitive Abilities
    ("Verify Interactive - Numerical", "Numerical reasoning and problem solving", "Cognitive", 18),
    ("Verify Interactive - Verbal", "Verbal reasoning and comprehension", "Cognitive", 18),
    ("Verify Interactive - Inductive", "Inductive reasoning and pattern recognition", "Cognitive", 18),
    ("Verify Interactive - Deductive", "Deductive reasoning and logical thinking", "Cognitive", 18),
    ("Numerical Reasoning", "Numerical problem solving and data interpretation", "Cognitive", 20),
    ("Verbal Reasoning", "Verbal comprehension and critical thinking", "Cognitive", 20),
    ("Abstract Reasoning", "Abstract pattern recognition", "Cognitive", 20),
    ("Logical Reasoning", "Logical problem solving", "Cognitive", 20),
    ("Spatial Reasoning", "Spatial awareness and visualization", "Cognitive", 15),
    ("Mechanical Reasoning", "Mechanical and technical reasoning", "Cognitive", 20),
    
    # Personality & Behavior
    ("OPQ32", "Occupational Personality Questionnaire - comprehensive personality assessment", "Personality & Behavior", 45),
    ("MQ", "Motivation Questionnaire - assesses workplace motivations", "Personality & Behavior", 30),
    ("Situational Judgment Test", "Workplace scenario judgment assessment", "Personality & Behavior", 25),
    ("Leadership Assessment", "Leadership style and capabilities", "Personality & Behavior", 30),
    ("Teamwork Assessment", "Team collaboration and interpersonal skills", "Personality & Behavior", 20),
    ("Communication Skills", "Verbal and written communication assessment", "Personality & Behavior", 25),
    ("Customer Service Aptitude", "Customer service skills and attitude", "Personality & Behavior", 20),
    ("Sales Aptitude", "Sales skills and personality fit", "Personality & Behavior", 25),
    ("Emotional Intelligence", "Emotional awareness and management", "Personality & Behavior", 20),
    
    # Business & Management
    ("Business Acumen", "Business knowledge and commercial awareness", "Knowledge & Skills", 25),
    ("Project Management", "Project management principles and practices", "Knowledge & Skills", 30),
    ("Financial Analysis", "Financial statement analysis and interpretation", "Knowledge & Skills", 25),
    ("Marketing Fundamentals", "Marketing concepts and strategies", "Knowledge & Skills", 20),
    ("Strategic Thinking", "Strategic planning and analysis", "Knowledge & Skills", 25),
    ("Risk Management", "Risk assessment and mitigation", "Knowledge & Skills", 20),
    
    # IT & Systems
    ("Network Administration", "Network configuration and management", "Knowledge & Skills", 25),
    ("Cybersecurity", "Information security principles and practices", "Knowledge & Skills", 30),
    ("Cloud Computing", "Cloud platforms and services", "Knowledge & Skills", 25),
    ("DevOps", "DevOps practices and tools", "Knowledge & Skills", 25),
    ("System Administration", "System administration and maintenance", "Knowledge & Skills", 25),
    ("Database Administration", "Database management and optimization", "Knowledge & Skills", 25),
    
    # Specialized Skills
    ("Accounting", "Accounting principles and practices", "Knowledge & Skills", 30),
    ("Legal Knowledge", "Legal concepts and terminology", "Knowledge & Skills", 30),
    ("Medical Terminology", "Healthcare and medical terminology", "Knowledge & Skills", 20),
    ("Engineering Principles", "Core engineering concepts", "Knowledge & Skills", 30),
    ("Quality Assurance", "QA testing methodologies", "Knowledge & Skills", 25),
    ("Technical Writing", "Technical documentation skills", "Knowledge & Skills", 20),
    ("Research Skills", "Research methodology and analysis", "Knowledge & Skills", 25),
]

def generate_mock_catalog(num_assessments=377):
    """Generate mock SHL assessment catalog"""
    print(f"Generating mock catalog with {num_assessments} assessments...")
    
    assessments = []
    base_assessments = ASSESSMENTS_DATA.copy()
    
    # Add base assessments
    for i, (name, desc, test_type, duration) in enumerate(base_assessments):
        assessments.append({
            "name": name,
            "url": f"https://www.shl.com/solutions/products/product-catalog/view/{name.lower().replace(' ', '-')}/",
            "description": desc,
            "duration": duration,
            "test_type": test_type,
            "remote_support": "Yes",
            "adaptive_support": random.choice(["Yes", "No"])
        })
    
    # Generate additional variations to reach target number
    variations = [
        "Advanced", "Intermediate", "Basic", "Professional", "Expert",
        "Level 1", "Level 2", "Level 3", "Comprehensive", "Essential"
    ]
    
    while len(assessments) < num_assessments:
        base = random.choice(base_assessments)
        variation = random.choice(variations)
        
        name = f"{base[0]} - {variation}"
        desc = f"{variation} {base[1]}"
        
        assessments.append({
            "name": name,
            "url": f"https://www.shl.com/solutions/products/product-catalog/view/{name.lower().replace(' ', '-').replace('--', '-')}/",
            "description": desc,
            "duration": base[3] + random.randint(-5, 5),
            "test_type": base[2],
            "remote_support": "Yes",
            "adaptive_support": random.choice(["Yes", "No"])
        })
    
    # Create DataFrame
    df = pd.DataFrame(assessments[:num_assessments])
    
    print(f"\nGenerated {len(df)} assessments")
    print(f"\nTest type breakdown:")
    print(df['test_type'].value_counts())
    
    # Save
    df.to_csv("data/raw/shl_catalog_raw.csv", index=False)
    print(f"\nSaved to data/raw/shl_catalog_raw.csv")
    
    return df

if __name__ == "__main__":
    generate_mock_catalog()
