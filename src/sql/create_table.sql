use neojune;

-- 기업정보
CREATE TABLE TB24_100 (
    company_seq INT AUTO_INCREMENT PRIMARY KEY,
    biz_no VARCHAR(12) NULL, 
    corp_no VARCHAR(15) NULL, 
    biz_type VARCHAR(5)  NULL,
    company_name VARCHAR(50)  NOT NULL
);

-- 대학 특허 고객번호
CREATE TABLE TB24_210(
    university_seq INT AUTO_INCREMENT PRIMARY KEY, 
    applicant_no BIGINT NULL,
    applicant  VARCHAR(500) NOT NULL,
    biz_no VARCHAR(12) NULL, 
    corp_no VARCHAR(15) NULL, 
    ref_desc VARCHAR(20) NULL, 
    write_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 기업 정보와 연동된 특허 고객번호 
CREATE TABLE TB24_200(
    applicant_id INT AUTO_INCREMENT PRIMARY KEY, 
    app_no VARCHAR(20) , 
    compay_name VARCHAR(50) , 
    corp_no VARCHAR(15),
    biz_no VARCHAR(12),
    company_seq INT,
    FOREIGN KEY (company_seq) REFERENCES TB24_100(company_seq)
);