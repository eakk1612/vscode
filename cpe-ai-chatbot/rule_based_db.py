# rule_based_db.py
rule_based_db = {
    
    # วิศวกรรมคอมพิวเตอร์ PSRU
    "วิศวกรรมคอมพิวเตอร์คืออะไร": "วิศวกรรมคอมพิวเตอร์เป็นหลักสูตรที่ผสานความรู้ด้านวิศวกรรมและคอมพิวเตอร์เพื่อพัฒนานวัตกรรมและแก้ปัญหาด้วยเทคโนโลยี",
    "เรียนวิศวกรรมคอมพิวเตอร์ยากไหม": "ขึ้นอยู่กับความถนัดด้านคณิตศาสตร์และการเขียนโปรแกรม แต่ถ้าฝึกอย่างต่อเนื่องจะเรียนได้",
    "มีวิชาอะไรบ้างในหลักสูตรวิศวกรรมคอมพิวเตอร์": "มีทั้ง Calculus, Physics, Programming, Digital System, AI, Machine Learning, Computer Networks และอื่น ๆ ตามหลักสูตรของ PSRU",
    "อาจารย์หลักในสาขานี้มีใครบ้าง": "เช่น ผู้ช่วยศาสตราจารย์ ดร. Wachira Limsripraphan, Ph.D., ผู้ช่วยศาสตราจารย์ Wanarat Juraphanthong, Ph.D. เป็นต้น",
    "จะติดต่อสาขาวิศวกรรมคอมพิวเตอร์ได้อย่างไร": "ติดต่อได้ที่อาคารปฏิบัติการหุ่นยนต์และระบบอัตโนมัติ คณะเทคโนโลยีอุตสาหกรรม, PSRU, โทร 055‑267004, Email: cpe_psru@psru.ac.th",
    "สาขาได้รับมาตรฐานคุณภาพใดบ้าง": "หลักสูตรได้รับการประเมินคุณภาพตามเกณฑ์ AUN‑QA",
    "เรียนวิชา AI มีอะไรบ้าง": "มี Artificial Intelligence, Expert Systems, Pattern Recognition, Machine Learning, Digital Image Processing",
    "สาขานี้ใช้แนวทางการเรียนแบบไหน": "หลักสูตรปรับปรุงตามแนวทาง OBE (Outcome-Based Education) และ CWIE (Cooperative Work Integrated Education)",
    "คณาจารย์สาขานี้จบจากไหน": "เช่น Ph.D. Computer Engineering, Naresuan University; M.S./B.S. Computer Science, PSRU",
    "หลักสูตรนี้เปิดสอนกี่ปี": "สาขาวิศวกรรมคอมพิวเตอร์ เปิดสอนแบบปริญญาตรี 4 ปี",
    "มีห้องปฏิบัติการอะไรบ้าง": "มีห้อง Lab คอมพิวเตอร์, Lab ไมโครคอนโทรลเลอร์, Lab Robotics, Lab Digital System, Lab AI/ML",
    "สาขามีโครงงานหรือโปรเจคอะไร": "นักศึกษาจะทำโครงงานตามสายวิชา เช่น Robotics, IoT, Software Development, AI/ML Project",
    "มีชมรมหรือกิจกรรมนักศึกษาไหม": "มีชมรมคอมพิวเตอร์ ชมรมหุ่นยนต์ และกิจกรรมแข่งขันโครงงานต่าง ๆ",
    "นักศึกษาจบไปทำงานอะไรได้บ้าง": "สามารถเป็น Software Developer, AI Engineer, Network Engineer, System Analyst, Embedded System Engineer, Data Scientist",
    "มีวิชาเลือกอะไรบ้าง": "มีวิชาเลือกตามความสนใจ เช่น Mobile App, Web Development, AI, IoT, Robotics, Cybersecurity",
    "สาขานี้มีทุนการศึกษาหรือไม่": "มีทุนการศึกษาและทุนฝึกงานสำหรับนักศึกษาที่มีผลการเรียนดีและผลงานโดดเด่น",
    "สาขานี้ทำวิจัยอะไรได้บ้าง": "วิจัยด้าน AI, Machine Learning, Robotics, Embedded System, Computer Vision, Cybersecurity"
}

def check_rule_based(question):
    for key in rule_based_db:
        if key in question:
            return rule_based_db[key]
    return None