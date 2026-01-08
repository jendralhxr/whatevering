import numpy as np
import pandas as pd

np.random.seed(42)

# grading scheme
grades = [
    (100, 85, "A", 4.0),
    (84, 80, "A-", 3.5),
    (79, 75, "B+", 3.25),
    (74, 70, "B", 3.0),
    (69, 65, "B-", 2.75),
    (64, 60, "C+", 2.5),
    (59, 55, "C", 2.0),
    (54, 50, "D", 1.0),
    (49, 0, "E", 0.0),
]

# simulate scores
for mean in np.arange(70, 100, 2):
        
    scores = np.random.normal(loc=mean, scale=15, size=200)
    scores = np.clip(scores, 0, 100)
    
    def assign_grade(score):
        for mx, mn, g, gp in grades:
            if mn <= score <= mx:
                return g, gp
        return None, None
    
    data = []
    for s in scores:
        g, gp = assign_grade(s)
        data.append((round(s,2), g, gp))
    
    df = pd.DataFrame(data, columns=["Score", "Grade", "GradePoint"])
    
    summary = df.groupby("Grade").size().reset_index(name="Students").sort_values("Grade")
    print(f"mean={mean:.1f}  avg_GPA={ df['GradePoint'].mean():.2f}")
    


#-----

grades = [
    (100, 85, 4.0),
    (84, 80, 3.5),
    (79, 75, 3.25),
    (74, 70, 3.0),
    (69, 65, 2.75),
    (64, 60, 2.5),
    (59, 55, 2.0),
    (54, 50, 1.0),
    (49, 0, 0.0),
]

def grade_point(score):
    for mx, mn, gp in grades:
        if mn <= score <= mx:
            return gp
    return 0.0

n_students = 200
std = 20


    scores = np.random.normal(loc=mean, scale=std, size=n_students)
    scores = np.clip(scores, 0, 100)

    gpas = [grade_point(s) for s in scores]
    avg_gpa = np.mean(gpas)

   
