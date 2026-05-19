-- Dummy Company Database Backup
-- Generated: 2026-05-19

CREATE DATABASE company_db;
USE company_db;

CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    status VARCHAR(50),
    department VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(20),
    salary INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO employees VALUES
(1, 'Nobel', 'active', 'IT', 'nobel@company.com', '081234567801', 12000000, NOW()),
(2, 'Admin', 'active', 'Management', 'admin@company.com', '081234567802', 18000000, NOW()),
(3, 'Rina', 'active', 'Finance', 'rina@company.com', '081234567803', 9500000, NOW()),
(4, 'Andi', 'inactive', 'HR', 'andi@company.com', '081234567804', 8700000, NOW()),
(5, 'Siska', 'active', 'Marketing', 'siska@company.com', '081234567805', 9100000, NOW());

CREATE TABLE login_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    ip_address VARCHAR(100),
    login_time DATETIME,
    status VARCHAR(50)
);

INSERT INTO login_logs (username, ip_address, login_time, status) VALUES
('admin', '192.168.1.10', '2026-05-19 08:10:11', 'success'),
('nobel', '192.168.1.20', '2026-05-19 08:15:44', 'success'),
('guest', '192.168.1.35', '2026-05-19 08:17:02', 'failed'),
('root', '10.0.0.1', '2026-05-19 08:20:55', 'failed'),
('kevin', '192.168.1.50', '2026-05-19 08:22:10', 'success');

CREATE TABLE files (
    file_id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    owner VARCHAR(100),
    file_size VARCHAR(20),
    upload_date DATETIME
);

INSERT INTO files (filename, owner, file_size, upload_date) VALUES
('laporan_keuangan.pdf', 'Rina', '2MB', NOW()),
('project_it_backup.zip', 'Kevin', '120MB', NOW()),
('employee_data.xlsx', 'Admin', '5MB', NOW()),
('marketing_plan.pptx', 'Siska', '12MB', NOW());

-- End of backup