-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 08, 2025 at 05:28 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jeska`
--

-- --------------------------------------------------------

--
-- Table structure for table `components`
--

CREATE TABLE `components` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `in_use` int(11) DEFAULT 0,
  `total` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `components`
--

INSERT INTO `components` (`id`, `name`, `type`, `description`, `in_use`, `total`) VALUES
(127, 'AMD Ryzen 5 1600', 'CPU', 'AMD Ryzen 5 1600, 6 nucleos, 3,20Ghz', 18, 18),
(128, 'AMD Ryzen 5 2600', 'CPU', 'AMD Ryzen 5 2600, 6 nucleos, 3.40Ghz', 10, 10),
(129, 'AMD Ryzen 5-1600', 'CPU', 'AMD Ryzen 5-1600, 6 nucleos, 3,20Ghz', 1, 1),
(130, 'Intel - H410M-E', 'CPU', 'Intel - H410M-E', 0, 4),
(131, 'Intel Celeron G1840', 'CPU', 'Intel Celeron G1840, 2 nucleos, 2.80Ghz', 4, 4),
(132, 'Intel Pentium G3220', 'CPU', 'Intel Pentium G3220, 2 nucleos, 3.00Ghz', 5, 5),
(133, 'Intel Pentium Gold G6405  ', 'CPU', 'Intel Pentium Gold G6405  , 2 nucleos, 4,10Ghz', 4, 4),
(134, 'Intel i3-4130', 'CPU', 'Intel i3-4130, 2 nucleos, 3.40Ghz', 14, 14),
(135, 'Intel i3-4150', 'CPU', 'Intel i3-4150, 2 nucleos, 3.50Ghz', 20, 20),
(136, 'Intel i3-4160', 'CPU', 'Intel i3-4160, 2 nucleos, 3.60Ghz', 6, 6),
(137, 'Intel i3-9100', 'CPU', 'Intel i3-9100, 4 nucleos, 3.60Ghz', 1, 1),
(138, 'Intel i5-10400', 'CPU', 'Intel i5-10400, 6 nucleos, 2.90Ghz', 5, 25),
(139, 'Intel i5-10500', 'CPU', 'Intel i5-10500, 6 nucleos, 3,10Ghz', 0, 6),
(140, 'Intel i5-11400F', 'CPU', 'Intel i5-11400F, 6 nucleos, 2,50Ghz', 1, 1),
(141, 'Intel i5-12400F', 'CPU', 'Intel i5-12400F, 12 nucleos, 2,50Ghz', 8, 8),
(142, 'Intel i5-2300', 'CPU', 'Intel i5-2300, 4 nucleos, 2.80Ghz', 1, 1),
(143, 'Intel i5-2320', 'CPU', 'Intel i5-2320, 4 nucleos, 3,00Ghz', 10, 10),
(144, 'Intel i5-2500s', 'CPU', 'Intel i5-2500s, 4 nucleos, 2.70Ghz', 4, 4),
(145, 'Intel i5-3330', 'CPU', 'Intel i5-3330, 4 nucleos, 3,00Ghz', 1, 1),
(146, 'Intel i5-3470', 'CPU', 'Intel i5-3470, 4 nucleos, 3,20Ghz', 7, 7),
(147, 'Intel i5-4460', 'CPU', 'Intel i5-4460, 4 nucleos, 3,20Ghz', 5, 5),
(148, 'Intel i5-6400', 'CPU', 'Intel i5-6400, 4 nucleos, 2,70Ghz', 11, 11),
(149, 'Intel i5-9400F', 'CPU', 'Intel i5-9400F, 6 nucleos, 2.90Ghz', 12, 12),
(150, 'Intel i7-13700', 'CPU', 'Intel i7-13700, 6 nucleos, 2,10Ghz', 0, 1),
(151, 'Intel i7-13700F', 'CPU', 'Intel i7-13700F, 16 nucleos, 2,10Ghz', 2, 2),
(152, 'Intel i7-2600', 'CPU', 'Intel i7-2600, 4 nucleos, 3,40Ghz', 3, 3),
(153, 'Inter i5-4430', 'CPU', 'Inter i5-4430, 4 nucleos, 3,00Ghz', 2, 2),
(154, 'intel - H510', 'CPU', 'intel - H510', 0, 2),
(155, 'KINGSTON 480', 'Disk', 'KINGSTON 480, 500GB SSD', 1, 1),
(156, 'KINGSTON SA2000M8500G', 'Disk', 'Kingston sa2000M8500G, 500GB HDD', 1, 3),
(157, 'KINGSTON SA400S37120G', 'Disk', 'KINGSTON SA400S37120G, 120GB SSD', 1, 1),
(158, 'KINGSTON SA400S37240', 'Disk', 'KINGSTON SA400S37240, 250GB SSD', 18, 18),
(159, 'KINGSTON SA400S37240G', 'Disk', 'Kingston SA400S37240G , 250GB HDD', 2, 1),
(160, 'KINGSTON SA400S37480G', 'Disk', 'KINGSTON SA400S37480G, 500GB HDD', 15, 15),
(161, 'KINGSTON SNV2S2000G', 'Disk', 'KINGSTON SNV2S2000G, 2TB SSD', 2, 3),
(162, 'KINGSTON SNVS1000G', 'Disk', 'KINGSTON SNVS1000G, 1TB SSD', 1, 1),
(163, 'KINGSTON SNVS500G', 'Disk', 'KINGSTON SNVS500G, 500GB NVMe', 1, 6),
(164, 'Kinston SA400S37480G', 'Disk', 'Kinston SA400S37480G, 500GB SSD', 1, 1),
(165, 'Kinston SNV2S1000G', 'Disk', 'Kinston SNV2S1000G, 1TB nmve', 1, 1),
(166, 'Kinston snv25', 'Disk', 'Kinston snv25, 1TB nmve', 8, 1),
(167, 'Kinston snv26', 'Disk', 'Kinston snv26, 1TB nmve', 0, 1),
(168, 'Kinston snv27', 'Disk', 'Kinston snv27, 1TB nmve', 0, 1),
(169, 'Kinston snv28', 'Disk', 'Kinston snv28, 1TB nmve', 0, 1),
(170, 'Kinston snv29', 'Disk', 'Kinston snv29, 1TB nmve', 0, 1),
(171, 'Kinston snv30', 'Disk', 'Kinston snv30, 1TB nmve', 0, 1),
(172, 'Kinston snv31', 'Disk', 'Kinston snv31, 1TB nmve', 0, 1),
(173, 'Kinston snv32', 'Disk', 'Kinston snv32, 1TB nmve', 0, 1),
(174, 'MAXTOR 6L200M0', 'Disk', 'MAXTOR 6L200M0, 200GB HDD', 0, 1),
(175, 'ModeloWDC WD10EZEX-08WN4A0', 'Disk', 'ModeloWDC WD10EZEX-08WN4A0, 1TB, HDD', 0, 1),
(176, 'ST1000DL002-9TT153', 'Disk', 'ST1000DL002-9TT153, 1TB HDD', 1, 1),
(177, 'ST1000DM003', 'Disk', 'ST1000DM003, 1TB, HDD', 1, 1),
(178, 'ST1000DM003-1C', 'Disk', 'ST1000DM003-1C, 1TB, HDD', 1, 1),
(179, 'ST1000DM003-1ER162', 'Disk', 'ST1000DM003-1ER162, 1TB HDD', 5, 5),
(180, 'ST1000DM003-1SB102', 'Disk', 'ST1000DM003-1SB102, 1TB, HDD', 2, 2),
(181, 'ST1000DM003-9YN162', 'Disk', 'ST1000DM003-9YN162, 1TB HDD', 5, 5),
(182, 'ST1000DM010-2EP102', 'Disk', 'ST1000DM010-2EP102, 1TB, HDD', 2, 2),
(183, 'ST2000DM008-2FR102 ', 'Disk', 'ST2000DM008-2FR102 , 2TB, HDD', 1, 1),
(184, 'ST250DM000-1BD14', 'Disk', 'ST250DM000-1BD14, 250GB HDD', 1, 1),
(185, 'ST250DM000-1BD141', 'Disk', 'ST250DM000-1BD141, 250GB HDD', 5, 5),
(186, 'ST31000528AS', 'Disk', 'ST31000528AS, 1TB HDD', 2, 2),
(187, 'ST500DM002-1BD142', 'Disk', 'ST500DM002-1BD142, 500GB HDD', 17, 17),
(188, 'Samsung 850 EVO', 'Disk', 'Samsung 850 EVO, 250GB SSD', 1, 1),
(189, 'Samsung ssd 850 pro 256gb ', 'Disk', 'Samsung ssd 850 pro 256gb , 250GB SSD', 1, 1),
(190, 'WD', 'Disk', 'WD, 1TB, HDD', 1, 1),
(191, 'WD WD10EZEX-08WN4A0', 'Disk', 'WD WD10EZEX-08WN4A0, 1TB, HDD', 3, 3),
(192, 'WD2500AAKX-07U6AA0', 'Disk', 'WD2500AAKX-07U6AA0, 250GB HDD', 4, 4),
(193, 'WD5000AAKX-00ERMA0', 'Disk', 'WD5000AAKX-00ERMA0, 500GB HDD', 3, 3),
(194, 'WD5000AAKX-08U6AA0', 'Disk', 'WD5000AAKX-08U6AA0, 500GB HDD', 1, 1),
(195, 'WDC WD10EALX-009BA0', 'Disk', 'WDC WD10EALX-009BA0, 1TB HDD', 1, 1),
(196, 'WDC WD10EZEX-08WN4A0', 'Disk', 'WDC WD10EZEX-08WN4A0 , 1TB HDD', 5, 1),
(197, 'WDC WD10EZRX-00A8LB0', 'Disk', 'WDC WD10EZRX-00A8LB0, 1TB, HDD', 1, 1),
(198, 'WDC WD10EZRX-00L4HB0', 'Disk', 'WDC WD10EZRX-00L4HB0, 1TB HDD', 1, 1),
(199, 'WDC WD2500AAKX-07U6AA0', 'Disk', 'WDC WD2500AAKX-07U6AA0, 250GB HDD', 4, 4),
(200, 'WDC WD2500AAKXAA0', 'Disk', 'WDC WD2500AAKXAA0, 250GB HDD', 1, 1),
(201, 'WDC WD5000AAKX-00ERMA0', 'Disk', 'WDC WD5000AAKX-00ERMA0 , 500GB HDD', 19, 3),
(202, 'WDC WD5000AAKX-08U6AA0', 'Disk', 'WDC WD5000AAKX-08U6AA0 , 500GB HDD', 12, 10),
(203, 'WDC WD5000AAKX-60U6AA0', 'Disk', 'WDC WD5000AAKX-60U6AA0, 500GB HDD', 1, 1),
(204, 'WDC WD5000AAKX-75U6AA0', 'Disk', 'WDC WD5000AAKX-75U6AA0, 500GB HDD', 1, 1),
(205, 'kingston sa200M85500G', 'Disk', 'kingston sa200M85500G, 500GB HDD', 1, 1),
(206, ' Asustek computer inc. H81M-E', 'Motherboard', 'Asustek computer inc. H81M-E', 0, 1),
(207, ' Asustek computer inc. H81M-Plus', 'Motherboard', 'Asustek computer inc. H81M-Plus', 0, 3),
(208, ' Gigabyte technology co,. Ltd. B450M DS3H-CF', 'Motherboard', 'Gigabyte technology co,. Ltd. B450M DS3H-CF', 0, 1),
(209, ' Gigabyte technology co,. Ltd. H510M H', 'Motherboard', 'Gigabyte technology co,. Ltd. H510M H', 0, 1),
(210, ' Gigabyte technology co,. Ltd. H61M USB3H', 'Motherboard', 'Gigabyte technology co,. Ltd. H61M USB3H', 0, 1),
(211, 'ASUS H110M-D', 'Motherboard', 'ASUS H110M-D', 8, 8),
(212, 'ASUS TUF Gaming B-660 plus', 'Motherboard', 'ASUS TUF Gaming B-660 plus', 1, 1),
(213, 'ASUS TUF Gaming B660 - PLUS ', 'Motherboard', 'ASUS TUF Gaming B660 - PLUS', 0, 1),
(214, 'Asus P8P67 EVO', 'Motherboard', 'Asus P8P67 EVO', 1, 1),
(215, 'Asus model H110M-D', 'Motherboard', 'Asus model H110M-D', 3, 3),
(216, 'Asus-P8p67evo', 'Motherboard', 'Asus-P8p67evo', 1, 1),
(217, 'Asustek computer inc. H81M-K', 'Motherboard', 'Asustek computer inc. H81M-K', 1, 1),
(218, 'Asustek computer inc. H81M-Plus', 'Motherboard', 'Asustek computer inc. H81M-Plus', 4, 1),
(219, 'Asustek computer inc. P8P67 evo', 'Motherboard', 'Asustek computer inc. P8P67 evo', 1, 1),
(220, 'Dell OptiPlex 3010', 'Motherboard', 'Dell OptiPlex 3010', 15, 15),
(221, 'Dell OptiPlex 3020', 'Motherboard', 'Dell OptiPlex 3020', 2, 2),
(222, 'Dell OptiPlex 3020 0WMJ54', 'Motherboard', 'Dell OptiPlex 3020 0WMJ54', 24, 24),
(223, 'GYBABYTE D450M D53H', 'Motherboard', 'GYBABYTE D450M D53H', 1, 1),
(224, 'Gibabyte - B460M DS3H V2', 'Motherboard', 'Gibabyte - B460M DS3H V2', 0, 19),
(225, 'Gibabyte - B460M DS3H V2 - VA MUY MUY LENTO. CAMBIAR DISCOS. ', 'Motherboard', 'Gibabyte - B460M DS3H V2 - VA MUY MUY LENTO. CAMBIAR DISCOS.', 0, 1),
(226, 'Gigabyte 310M ', 'Motherboard', 'Gigabyte 310M', 1, 1),
(227, 'Gigabyte B560M DS3H V2', 'Motherboard', 'Gigabyte B560M DS3H V2', 1, 1),
(228, 'Gigabyte B85M-DS3H', 'Motherboard', 'Gigabyte B85M-DS3H', 1, 1),
(229, 'Gigabyte H310M ', 'Motherboard', 'Gigabyte H310M', 1, 1),
(230, 'Gigabyte H310M PRO-M2 PLUS (MS-7C08)', 'Motherboard', 'Gigabyte H310M PRO-M2 PLUS (MS-7C08)', 6, 6),
(231, 'Gigabyte H410M PRO-M2 PLUS (MS-7C08)', 'Motherboard', 'Gigabyte H410M PRO-M2 PLUS (MS-7C08)', 1, 1),
(232, 'Gigabyte H410M S2H', 'Motherboard', 'Gigabyte H410M S2H', 2, 2),
(233, 'Gigabyte H81M-D2V', 'Motherboard', 'Gigabyte H81M-D2V', 3, 3),
(234, 'Gigabyte Technology Co. Ltd. B85M-DS3H', 'Motherboard', 'Gigabyte Technology Co. Ltd. B85M-DS3H', 2, 2),
(235, 'Gigabyte Technology co., Ltd. B85M-DS3H', 'Motherboard', 'Gigabyte Technology co., Ltd. B85M-DS3H', 0, 1),
(236, 'H310M PRO M2 PLUS', 'Motherboard', 'H310M PRO M2 PLUS', 3, 3),
(237, 'H310M S2H 2.0', 'Motherboard', 'H310M S2H 2.0', 1, 1),
(238, 'H410M S2H', 'Motherboard', 'H410M S2H', 2, 2),
(239, 'H81M PLUS ', 'Motherboard', 'H81M PLUS', 1, 1),
(240, 'H81M-D2V', 'Motherboard', 'H81M-D2V', 1, 1),
(241, 'H81M2-1M-D2V', 'Motherboard', 'H81M2-1M-D2V', 1, 1),
(242, 'HP Compaq Elite 8300 USDT   3398', 'Motherboard', 'HP Compaq Elite 8300 USDT   3398', 7, 7),
(243, 'HP ProDesk 600 G1 SFF', 'Motherboard', 'HP ProDesk 600 G1 SFF', 14, 14),
(244, 'Micro-Star International Co., Ltd. H310M pro m2 Plus(ms-7C08)', 'Motherboard', 'Micro-Star International Co., Ltd. H310M pro m2 Plus(ms-7C08)', 0, 1),
(245, 'PRO B760M-PDDR4', 'Motherboard', 'PRO B760M-PDDR4', 8, 8),
(246, 'TICNOVA E70 SFF', 'Motherboard', 'TICNOVA E70 SFF', 10, 10),
(247, 'TUF GAMING B660-PLUS WIFI D4', 'Motherboard', 'TUF GAMING B660-PLUS WIFI D4', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `configurations`
--

CREATE TABLE `configurations` (
  `name` varchar(255) NOT NULL,
  `options` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `configurations`
--

INSERT INTO `configurations` (`name`, `options`) VALUES
('COMPONENT_TYPES', 'CPU,RAM,Disk,Power supply,Motherboard,Others'),
('DEVICE_STATUSES', 'Active,Maintenance,Inactive'),
('LOCATIONS', '1013,1014,1015,1109,1115,1119,1120,1113,1111,Storage'),
('PERIPHERAL_TYPES', 'Screen,Mouse,Keyboard,Printer,Others'),
('REPORT_STATUSES', 'Open,In Progress,Closed');

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE `devices` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `components` varchar(255) DEFAULT NULL,
  `peripherals` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `buying_timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `mac_address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `devices`
--

INSERT INTO `devices` (`id`, `name`, `description`, `status`, `components`, `peripherals`, `location`, `buying_timestamp`, `mac_address`) VALUES
(424, '1013PC00', 'Student\'s PC', 'Active', 'Gigabyte B560M DS3H V2,Intel i5-11400F,Kinston SNV2S1000G', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '74-56-3C-65-5F-ED'),
(425, '1013PC01', 'Student\'s PC', 'Active', 'Gigabyte H81M-D2V,Intel Pentium G3220,WD5000AAKX-08U6AA0', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '74-D4-35-2C-8B-ED'),
(426, '1013PC02', 'Student\'s PC', 'Active', 'Gigabyte H81M-D2V,Intel Pentium G3220,WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '74-D4-35-2C-F4-0B'),
(427, '1013PC03', 'Student\'s PC', 'Active', 'Gigabyte H81M-D2V,Intel Pentium G3220,WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '74-D4-35-2C-90-32'),
(428, '1013PC04', 'Student\'s PC', 'Active', 'Gigabyte B85M-DS3H,Intel Celeron G1840,WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', 'FC-AA-14-45-13-C1'),
(429, '1013PC05', 'puesto sin torre para reparaciones (monitor, ratón y teclado)', 'Inactive', '', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', ''),
(430, '1013PC06', 'puesto sin torre para reparaciones (monitor, ratón y teclado)', 'Inactive', '', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', ''),
(431, '1014PC07', 'puesto sin torre para reparaciones (monitor, ratón y teclado)', 'Inactive', '', 'Mouse,Keyboard,Screen', '1014', '2024-03-20 09:00:00', ''),
(432, '1015PC08', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020,Intel i3-4150,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'B0-83-FE-58-9E-69'),
(433, '1013PC09', 'puesto sin torre para reparaciones (monitor, ratón y teclado)', 'Inactive', '', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', ''),
(434, '1013PC10', 'puesto sin torre para reparaciones (monitor, ratón y teclado)', 'Inactive', '', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', ''),
(435, '1013PC11', 'puesto sin torre para reparaciones (monitor, ratón y teclado)', 'Inactive', '', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', ''),
(436, '1013PC12', 'puesto sin torre para reparaciones (monitor, ratón y teclado)', 'Inactive', '', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', ''),
(437, '1013PC13', 'Student\'s PC', 'Active', 'PRO B760M-PDDR4,Intel i5-12400F,Kinston snv25', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '74-56-3C-91-76-BF'),
(438, '1013PC14', 'Student\'s PC', 'Active', 'PRO B760M-PDDR4,Intel i5-12400F,Kinston snv25', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '04-7C-16-E8-C8-24'),
(439, '1013PC15', 'Student\'s PC', 'Active', 'PRO B760M-PDDR4,Intel i5-12400F,Kinston snv25', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '04-7C-16-E8-C8-44'),
(440, '1013PC16', 'Student\'s PC', 'Active', 'PRO B760M-PDDR4,Intel i5-12400F,Kinston snv25', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '04-7C-16-E8-C8-21'),
(441, '1013PC17', 'Student\'s PC', 'Active', 'PRO B760M-PDDR4,Intel i5-12400F,Kinston snv25', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '04-7C-16-EE-EF-96'),
(442, '1013PC18', 'Student\'s PC', 'Active', 'PRO B760M-PDDR4,Intel i5-12400F,Kinston snv25', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '04-7C-16-E8-C8-14'),
(443, '1013PC19', 'Student\'s PC', 'Active', 'PRO B760M-PDDR4,Intel i5-12400F,Kinston snv25', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '04-7C-16-E8-C8-2A'),
(444, '1013PC20', 'Student\'s PC', 'Active', 'PRO B760M-PDDR4,Intel i5-12400F,Kinston snv25', 'Mouse,Keyboard,Screen', '1013', '2024-03-20 09:00:00', '04-7C-16-E8-C8-3B'),
(445, '1015PC00', 'Student\'s PC', 'Active', 'H310M S2H 2.0,Intel i3-9100,KINGSTON SA400S37240G', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'B4-2E-99-DD-47-D4'),
(446, '1015PC01', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-E7-DE-52'),
(447, '1015PC02', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2300,ST250DM000-1BD141', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', '78-45-C4-1E-E0-61'),
(448, '1015PC03', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-EB-8F-25'),
(449, '1015PC04', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2320,WDC WD2500AAKXAA0', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', '78-45-C4-2D-16-62'),
(450, '1015PC05', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-EB-8F-A8'),
(451, '1015PC06', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2320,WDC WD2500AAKX-07U6AA0', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'A4-1F-72-82-C3-E8'),
(452, '1015PC07', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2320,WDC WD2500AAKX-07U6AA0', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'A4-1F-72-95-D7-7E'),
(454, '1015PC09', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-E7-DD-EF'),
(455, '1015PC10', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-EC-07-19'),
(456, '1015PC11', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-E7-DC-BF'),
(457, '1015PC12', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-E7-DE-60'),
(458, '1015PC13', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-E7-DD-E6'),
(459, '1015PC14', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2500s,ST250DM000-1BD141', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'A4-1F-72-82-C9-4B'),
(460, '1015PC15', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2320,WD2500AAKX-07U6AA0', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', '78-45-C4-12-E0-DC'),
(461, '1015PC16', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2320,WDC WD2500AAKX-07U6AA0', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'C8-1F-66-00-98-D2'),
(462, '1015PC17', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2320,WDC WD2500AAKX-07U6AA0', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'A4-1F-72-53-D3-A1'),
(463, '1015PC18', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020,Intel i3-4160,WDC WD5000AAKX-75U6AA0', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'B0-83-FE-94-D0-9B'),
(464, '1015PC19', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2320,ST250DM000-1BD141', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'A4-1F-72-63-21-5C'),
(465, '1015PC20', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2500s,ST250DM000-1BD14', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'A4-1F-72-82-2B-03'),
(466, '1015PC21', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2320,WD2500AAKX-07U6AA0', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'C8-1F-66-1C-C6-C7'),
(467, '1015PC22', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2320,WD2500AAKX-07U6AA0', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'A4-1F-72-5D-7E-04'),
(468, '1015PC23', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2500s,ST250DM000-1BD141', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'A4-1F-72-82-C9-9C'),
(469, '1015PC24', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2320,WD2500AAKX-07U6AA0', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'A4-1F-72-5C-3C-F6'),
(470, '1015PC25', 'Student\'s PC', 'Active', 'Dell OptiPlex 3010,Intel i5-2500s,ST250DM000-1BD141', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'A4-1F-72-81-FA-54'),
(471, '1015PC26', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-E7-DE-67'),
(472, '1015PC27', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-E2-77-0B'),
(473, '1015PC28', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-EB-8F-3C'),
(474, '1015PC29', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-EB-8D-BE'),
(475, '1015PC30', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-E2-78-50'),
(476, '1015PC31', 'Student\'s PC', 'Active', 'HP ProDesk 600 G1 SFF,Intel i3-4130,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1015', '2024-03-20 09:00:00', 'F0-92-1C-EB-8F-13'),
(477, '1109PC00', 'Student\'s PC', 'Active', ' Gigabyte technology co,. Ltd. B450M DS3H-CF,AMD Ryzen 5-1600,Samsung ssd 850 pro 256gb ,ST2000DM008-2FR102 ', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', '7C-8B-CA-01-B1-05'),
(478, '1109PC01', 'Student\'s PC', 'Active', ' Gigabyte technology co,. Ltd. H510M H  ,Intel Pentium Gold G6405  ,Kingston SA400S37240G', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', 'D8-5E-D3-A6-D2-56'),
(479, '1109PC10', 'Student\'s PC', 'Active', ' Asustek computer inc. H81M-Plus,Intel i5-4460,ST1000DM003-1ER162', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', '84-16-F9-04-6D-B7'),
(480, '1109PC11', 'Student\'s PC', 'Active', ' Asustek computer inc. H81M-Plus,Intel i5-4460,ST1000DM003-9YN162', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', '84-16-F9-04-B0-5A'),
(481, '1109PC12', 'Student\'s PC', 'Active', 'Asustek computer inc. H81M-Plus,Intel i5-4460,ST1000DM003-9YN162', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', '84-16-F9-04-19-A9'),
(482, '1109PC13', 'Student\'s PC', 'Active', 'Asustek computer inc. H81M-K,Intel i5-4460,ST1000DM003-1ER162', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', '84-16-F9-03-DF-D8'),
(483, '1109PC14', 'Student\'s PC', 'Active', ' Asustek computer inc. H81M-E,Inter i5-4430,WDC WD10EZRX-00L4HB0', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', '84-16-F9-04-43-92'),
(484, '1109PC15', 'Student\'s PC', 'Active', ' Asustek computer inc. H81M-Plus,Inter i5-4430,ST1000DM003-1ER162', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', '84-16-F9-04-37-35'),
(485, '1109PC16', 'Student\'s PC', 'Active', 'Gigabyte Technology co., Ltd. B85M-DS3H,Intel Celeron G1840,ST1000DM003-1ER162', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', 'FC-AA-14-44-2A-C0'),
(486, '1109PC17', 'Student\'s PC', 'Active', 'Asus model H110M-D,Intel i5-6400,WDC WD10EZEX-08WN4A0', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', '2C-4D-54-D5-08-4D'),
(487, '1109PC18', 'Student\'s PC', 'Active', 'Asus model H110M-D,Intel i5-6400,WDC WD10EZEX-08WN4A0', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', '2C-4D-54-D5-03-15'),
(488, '1109PC19', 'Student\'s PC', 'Active', 'Asus-P8p67evo,Intel i7-2600,ST31000528AS', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', 'F4-6D-04-98-F1-58'),
(489, '1109PC02', 'Student\'s PC', 'Active', ' Gigabyte technology co,. Ltd. H510M H ,Intel Pentium Gold G6405  ,Kingston SA400S37240G ', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', 'D8-5E-D3-A6-D1-DD'),
(490, '1109PC20', 'Student\'s PC', 'Active', 'Asus model H110M-D,Intel i5-6400,WDC WD10EZEX-08WN4A0 ', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', '2C-4D-54-D5-10-0D'),
(491, '1109PC03', 'Student\'s PC', 'Active', ' Gigabyte technology co,. Ltd. H510M H,Intel Pentium Gold G6405  ,KINGSTON SA400S37240G', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', 'D8-5E-D3-A6-F4-11'),
(492, '1109PC04', 'Student\'s PC', 'Active', ' Gigabyte technology co,. Ltd. H510M H,Intel Pentium Gold G6405  ,KINGSTON SA400S37240G', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', 'D8-5E-D3-A6-F4-21'),
(493, '1109PC05', 'Student\'s PC', 'Active', ' Gigabyte technology co,. Ltd. H61M USB3H,Intel i5-3330,KINGSTON SA400S37480G,ST1000DM003-1C', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', '74-D4-35-6B-B3-DE'),
(494, '1109PC06', 'Student\'s PC', 'Active', 'Gigabyte Technology Co. Ltd. B85M-DS3H,Intel Celeron G1840,KINGSTON SA400S37480G', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', 'FC-AA-14-46-6A-D6'),
(495, '1109PC07', 'Student\'s PC', 'Active', 'Gigabyte Technology Co. Ltd. B85M-DS3H,Intel Celeron G1840,KINGSTON SA400S37480G', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', 'FC-AA-14-43-50-D6'),
(496, '1109PC08', 'Student\'s PC', 'Active', 'Asustek computer inc. P8P67 evo,Intel i7-2600,ST1000DL002-9TT153', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', 'F4-6D-04-98-F1-68'),
(497, '1109PC09', 'Student\'s PC', 'Active', 'Asus P8P67 EVO,Intel i7-2600,WDC WD10EALX-009BA0', 'Mouse,Keyboard,Screen', '1109', '2024-03-20 09:00:00', 'F4-6D-04-99-02-3A'),
(498, '1115PC00', 'Student\'s PC', 'Active', 'TUF GAMING B660-PLUS WIFI D4,Intel i7-13700F,KINGSTON SNV2S2000G', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', 'C8-7F-54-05-BC-E3'),
(499, '1115PC01', 'Student\'s PC', 'Active', 'ASUS H110M-D,Intel i5-6400,KINGSTON 480,WD', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', '2C-4D-54-D5-08-45'),
(500, '1115PC02', 'Student\'s PC', 'Active', 'ASUS H110M-D,Intel i5-6400,Samsung 850 EVO,WDC WD10EZEX-08WN4A0', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', '2C-4D-54-D5-10-C2'),
(501, '1115PC03', 'Student\'s PC', 'Active', 'ASUS H110M-D,Intel i5-6400,KINGSTON SA400S37480G,Modelo\nWDC WD10EZEX-08WN4A0\n', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', '2C-4D-54-D5-06-C1'),
(502, '1115PC04', 'Student\'s PC', 'Active', 'ASUS H110M-D,Intel i5-6400,KINGSTON SA400S37480G,WDC WD10EZEX-08WN4A0', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', '2C-4D-54-D5-08-4B'),
(503, '1115PC05', 'Student\'s PC', 'Active', 'ASUS H110M-D,Intel i5-6400,KINGSTON SA400S37480G,ST1000DM010-2EP102', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', '18-31-BF-25-9D-AA'),
(504, '1115PC06', 'Student\'s PC', 'Active', 'ASUS H110M-D,Intel i5-6400,KINGSTON SA400S37480G,WD WD10EZEX-08WN4A0', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', '2C-4D-54-D5-08-4C'),
(505, '1115PC07', 'Student\'s PC', 'Active', 'ASUS H110M-D,Intel i5-6400,KINGSTON SA400S37480G,WD WD10EZEX-08WN4A0', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', '2C-4D-54-D4-F6-25'),
(506, '1115PC08', 'Student\'s PC', 'Active', 'ASUS H110M-D,Intel i5-6400,KINGSTON SA400S37480G,WD WD10EZEX-08WN4A0', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', '2C-4D-54-D4-F6-FA'),
(507, '1115PC09', 'Student\'s PC', 'Active', 'TICNOVA E70 SFF,AMD Ryzen 5 2600,KINGSTON SA400S37240,KINGSTON SA400S37240', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', 'A8:A1:59:5A:A7:EA'),
(508, '1115PC10', 'Student\'s PC', 'Active', 'TICNOVA E70 SFF,AMD Ryzen 5 2600,KINGSTON SA400S37240,KINGSTON SA400S37240', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', 'A8:A1:59:5A:A5:91'),
(509, '1115PC11', 'Student\'s PC', 'Active', 'TICNOVA E70 SFF,AMD Ryzen 5 2600,KINGSTON SA400S37240,KINGSTON SA400S37240', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', 'A8:A1:59:5A:9C:19'),
(510, '1115PC12', 'Student\'s PC', 'Active', 'TICNOVA E70 SFF,AMD Ryzen 5 2600,KINGSTON SA400S37240,KINGSTON SA400S37240', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', 'A8:A1:59:5A:A8:2C'),
(511, '1115PC13', 'Student\'s PC', 'Active', 'TICNOVA E70 SFF,AMD Ryzen 5 2600,KINGSTON SA400S37240,KINGSTON SA400S37240', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', 'A8:A1:59:52:EF:E4'),
(512, '1115PC14', 'Student\'s PC', 'Active', 'TICNOVA E70 SFF,AMD Ryzen 5 2600,KINGSTON SA400S37240,KINGSTON SA400S37240', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', 'A8:A1:59:5A:A7:7A'),
(513, '1115PC15', 'Student\'s PC', 'Active', 'TICNOVA E70 SFF,AMD Ryzen 5 2600,KINGSTON SNVS1000G', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', 'A8-A1-59-5F-2D-D5'),
(514, '1115PC16', 'Student\'s PC', 'Active', 'TICNOVA E70 SFF,AMD Ryzen 5 2600,KINGSTON SA400S37240,KINGSTON SA400S37240', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', 'A8:A1:59:5A:A9:55'),
(515, '1115PC17', 'Student\'s PC', 'Active', 'TICNOVA E70 SFF,AMD Ryzen 5 2600,KINGSTON SA400S37240,KINGSTON SA400S37240', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', 'A8:A1:59:5A:A0:29'),
(516, '1115PC18', 'Student\'s PC', 'Active', 'TICNOVA E70 SFF,AMD Ryzen 5 2600,KINGSTON SA400S37240,KINGSTON SA400S37240', 'Mouse,Keyboard,Screen', '1115', '2024-03-20 09:00:00', 'A8:A1:59:5A:A7:F0'),
(517, '1119PC00', 'Student\'s PC', 'Active', 'ASUS TUF Gaming B-660 plus,Intel i7-13700F,KINGSTON SNV2S2000G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', 'C8-7F-54-05-B7-B7'),
(518, '1119PC01', 'Student\'s PC', 'Active', 'Gigabyte H410M S2H,Intel i5-10400,Kingston sa2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '18-C0-4D-03-43-0F'),
(519, '1119PC02', 'Student\'s PC', 'Active', 'H310M PRO M2 PLUS,Intel i5-9400F,kingston sa200M85500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '00-D8-61-D9-D9-8A'),
(520, '1119PC03', 'Student\'s PC', 'Active', 'H310M PRO M2 PLUS,Intel i5-9400F,Kingston sa2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '00-D8-61-D9-D9-DE'),
(521, '1119PC04', 'Student\'s PC', 'Active', 'H310M PRO M2 PLUS,Intel i5-9400F,Kingston sa2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '00-D8-61-D9-D9-A0'),
(522, '1119PC05', 'Student\'s PC', 'Active', 'H410M S2H,Intel i5-10400,Kingston SA2000M8500G ', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '18-C0-4D-01-AA-58'),
(523, '1119PC06', 'Student\'s PC', 'Active', 'Gigabyte 310M ,Intel i5-10400,Kingston SA2000M8500G ', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '00-D8-61-CA-04-3C'),
(524, '1119PC07', 'Student\'s PC', 'Active', 'Gigabyte H310M PRO-M2 PLUS (MS-7C08),Intel i5-9400F,Kingston SA2000M8500G ', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '00-D8-61-D9-D9-D0'),
(525, '1119PC08', 'Student\'s PC', 'Active', 'Gigabyte H310M PRO-M2 PLUS (MS-7C08),Intel i5-9400F,Kingston SA2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '00-D8-61-D9-D9-92'),
(526, '1119PC09', 'Student\'s PC', 'Active', 'Gigabyte H310M PRO-M2 PLUS (MS-7C08),Intel i5-9400F,Kingston SA2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '00-D8-61-D9-D9-85'),
(527, '1119PC10', 'Student\'s PC', 'Active', 'H81M-D2V,Intel Pentium G3220,Kingston SA2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '74-D4-35-2C-93-C3'),
(528, '1119PC11', 'Student\'s PC', 'Active', 'H81M PLUS ,Intel i5-4460,Kingston SA2000M8500G ,ST1000DM010-2EP102', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '40-16-7E-AC-DB-7A'),
(529, '1119PC12', 'Student\'s PC', 'Inactive', 'Gigabyte H310M PRO-M2 PLUS (MS-7C08),Intel i5-9400F,Kingston SA2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', ''),
(530, '1119PC13', 'Student\'s PC', 'Active', 'Gigabyte H310M PRO-M2 PLUS (MS-7C08),Intel i5-9400F,Kingston SA2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '00-D8-61-D9-D9-E0'),
(531, '1119PC14', 'Student\'s PC', 'Active', 'Gigabyte H310M ,Intel i5-9400F,Kingston SA2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '00-D8-61-D9-DB-6E'),
(532, '1119PC15', 'Student\'s PC', 'Active', 'Gigabyte H410M PRO-M2 PLUS (MS-7C08),Intel i5-9400F,Kingston SA2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '18-C0-4D-03-68-0F'),
(533, '1119PC16', 'Student\'s PC', 'Active', 'Micro-Star International Co., Ltd. H310M pro m2 Plus(ms-7C08),Intel i5-9400F,Kingston SA2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '00-D8-61-D9-D9-E8'),
(534, '1119PC17', 'Student\'s PC', 'Active', 'Gigabyte H310M PRO-M2 PLUS (MS-7C08),Intel i5-9400F,Kingston SA2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '00-D8-61-D9-D9-D6'),
(535, '1119PC18', 'Student\'s PC', 'Active', 'H410M S2H,Intel i5-10400,Kingston SA2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '18-C0-4D-03-34-8F'),
(536, '1119PC19', 'Student\'s PC', 'Active', 'H81M2-1M-D2V,Intel Pentium G3220,WDC WD5000AAKX-08U6AA0 ', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '74-D4-35-2C-94-E5'),
(537, '1119PC20', 'Student\'s PC', 'Active', 'Gigabyte H410M S2H,Intel i5-10400,Kingston SA2000M8500G', 'Mouse,Keyboard,Screen', '1119', '2024-03-20 09:00:00', '18-C0-4D-03-80-9F'),
(538, '1120PC00', 'Student\'s PC', 'Active', 'GYBABYTE D450M D53H,AMD Ryzen 5 1600,Kinston SA400S37480G,ST31000528AS', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'E0-D5-5E-AD-5E-A3'),
(539, '1120PC01', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-57-E9-6C'),
(540, '1120PC02', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-08U6AA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-57-E8-FB'),
(541, '1120PC03', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-00ERMA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-58-AD-B0'),
(542, '1120PC04', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-00ERMA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-5C-A9-59'),
(543, '1120PC05', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-08U6AA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-59-30-CB'),
(544, '1120PC06', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-08U6AA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-58-A7-48'),
(545, '1120PC07', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-08U6AA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-59-66-26'),
(546, '1120PC08', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-08U6AA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-8F-A1-8A'),
(547, '1120PC09', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-5D-8D-B5'),
(548, '1120PC10', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-08U6AA0', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-57-E8-24'),
(549, '1120PC11', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4160,WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-8F-3A-45'),
(550, '1120PC12', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-59-66-29'),
(551, '1120PC13', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-57-EA-24'),
(552, '1120PC14', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-57-E3-E7'),
(553, '1120PC15', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4160,WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-8F-A3-F5'),
(554, '1120PC16', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-08U6AA0', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-58-A1-57'),
(555, '1120PC17', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-08U6AA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-5D-8E-0B'),
(556, '1120PC18', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-08U6AA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-57-E9-5E'),
(557, '1120PC19', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4160,WDC WD5000AAKX-08U6AA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-8F-A3-4E'),
(558, '1120PC20', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-58-A6-F6'),
(559, '1120PC21', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-08U6AA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-58-A1-0C'),
(560, '1120PC22', 'Student\'s PC', 'Active', 'HP Compaq Elite 8300 USDT   3398,Intel i5-3470,KINGSTON SA400S37120G', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'D4-C9-EF-D6-18-8B'),
(561, '1120PC23', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4160,WDC WD5000AAKX-60U6AA0', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-94-CC-D8'),
(562, '1120PC24', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4150,WDC WD5000AAKX-00ERMA0 ', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-58-6F-77'),
(563, '1120PC25', 'Student\'s PC', 'Active', 'Dell OptiPlex 3020 0WMJ54,Intel i3-4160,ST500DM002-1BD142', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'B0-83-FE-94-F8-C8'),
(564, '1120PC26', 'Student\'s PC', 'Active', 'HP Compaq Elite 8300 USDT   3398,Intel i5-3470,KINGSTON SA400S37480G', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', '28-92-4A-CC-32-44'),
(565, '1120PC27', 'Student\'s PC', 'Active', 'HP Compaq Elite 8300 USDT   3398,Intel i5-3470,KINGSTON SA400S37480G', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', '88-51-FB-81-C1-67'),
(566, '1120PC28', 'Student\'s PC', 'Active', 'HP Compaq Elite 8300 USDT   3398,Intel i5-3470,KINGSTON SA400S37480G', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'D8-D3-85-94-8F-2F'),
(567, '1120PC29', 'Student\'s PC', 'Active', 'HP Compaq Elite 8300 USDT   3398,Intel i5-3470,KINGSTON SA400S37480G', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', '28-92-4A-CC-0E-C4'),
(568, '1120PC30', 'Student\'s PC', 'Active', 'HP Compaq Elite 8300 USDT   3398,Intel i5-3470,KINGSTON SA400S37480G', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', 'D8-D3-85-94-8F-B1'),
(569, '1120PC31', 'Student\'s PC', 'Active', 'HP Compaq Elite 8300 USDT   3398,Intel i5-3470,KINGSTON SA400S37480G', 'Mouse,Keyboard,Screen', '1120', '2024-03-20 09:00:00', '28-92-4A-C8-58-D0'),
(570, '1113PC00', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:A2:55'),
(571, '1113PC01', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:9D:21'),
(572, '1113PC02', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:A8:5D'),
(573, '1113PC03', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:A5:6D'),
(574, '1113PC04', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:A5:E0'),
(575, '1113PC05', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:9B:ED'),
(576, '1113PC06', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:9D:46'),
(577, '1113PC07', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:A5:5B'),
(578, '1113PC08', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:9B:A2'),
(579, '1113PC09', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:A0:69'),
(580, '1113PC10', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:9D:0E'),
(581, '1113PC11', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:A5:9D'),
(582, '1113PC12', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:9E:D5'),
(583, '1113PC13', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:9C:96'),
(584, '1113PC14', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5F:2D:EC'),
(585, '1113PC15', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:A5:D9'),
(586, '1113PC16', 'Student\'s PC', 'Active', 'AMD Ryzen 5 1600', 'Mouse,Keyboard,Screen', '1113', '2024-03-20 09:00:00', 'A8:A1:59:5A:A9:74'),
(587, '111100', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', 'E0-D5-5E-AD-5E-A3'),
(588, '111101', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-97-20-D5'),
(589, '111102', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-8E-46'),
(590, '111103', 'Student\'s PC', 'Active', 'KINGSTON SA2000M8500G', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-81-D7'),
(591, '111104', 'Student\'s PC', 'Active', 'ST1000DM003', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-82-85'),
(592, '111105', 'Student\'s PC', 'Active', 'WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-E6-4C'),
(593, '111106', 'Student\'s PC', 'Active', 'ST1000DM003-9YN162', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-8E-33'),
(594, '111107', 'Student\'s PC', 'Active', 'WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-8E-67'),
(595, '111108', 'Student\'s PC', 'Active', 'ST1000DM003-9YN162', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-82-F5'),
(596, '111109', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', ' 18-C0-4D-97-1B-56'),
(597, '111110', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-ED-BD-B2'),
(598, '111111', 'Student\'s PC', 'Active', 'ST1000DM003-1SB102', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-97-56-AA'),
(599, '111112', 'Student\'s PC', 'Active', 'ST1000DM003-9YN162', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-97-4D-E1'),
(600, '111113', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-EE-D9-77'),
(601, '111114', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-EE-D9-11'),
(602, '111115', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-ED-BD-AE'),
(603, '111116', 'Student\'s PC', 'Active', 'WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-82-9C'),
(604, '111117', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-EB-9D'),
(605, '111118', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-ED-BD-1E'),
(606, '111119', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-ED-BD-AE'),
(607, '111120', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-EE-D9-74'),
(608, '111121', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-EE-D6-B1'),
(609, '111122', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-8E-5A'),
(610, '111123', 'Student\'s PC', 'Active', 'WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-82-97'),
(611, '111124', 'Student\'s PC', 'Active', 'WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-97-1B-3F'),
(612, '111125', 'Student\'s PC', 'Active', 'ST1000DM003-1SB102', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-97-15-83'),
(613, '111126', 'Student\'s PC', 'Active', 'WDC WD10EZRX-00A8LB0', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-8E-81\n'),
(614, '111127', 'Student\'s PC', 'Active', '', '', '1111', '2024-03-20 09:00:00', ' 00-E0-4C-EE-D6-17'),
(615, '111128', 'Student\'s PC', 'Active', 'WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-EE-D5-D0'),
(616, '111129', 'Student\'s PC', 'Active', 'WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-81-AC'),
(617, '111130', 'Student\'s PC', 'Active', 'WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-EE-D6-29'),
(618, '111131', 'Student\'s PC', 'Active', 'ST1000DM003-1ER162', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-14-4B-99'),
(619, '111132', 'Student\'s PC', 'Active', 'KINGSTON SNVS500G', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '00-E0-4C-14-4C-55'),
(620, '111133', 'Student\'s PC', 'Active', 'WDC WD5000AAKX-00ERMA0', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', '18-C0-4D-96-83-43'),
(621, '111134', 'Student\'s PC', 'Active', '', 'Mouse,Keyboard,Screen', '1111', '2024-03-20 09:00:00', 'C8-7F-54-05-B7-89');

-- --------------------------------------------------------

--
-- Table structure for table `peripherals`
--

CREATE TABLE `peripherals` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `in_use` int(11) DEFAULT 0,
  `total` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `peripherals`
--

INSERT INTO `peripherals` (`id`, `name`, `type`, `description`, `in_use`, `total`) VALUES
(4, 'Mouse', 'Mouse', '', 196, 200),
(5, 'Keyboard', 'Keyboard', '', 196, 200),
(6, 'Screen', 'Screen', '', 196, 200);

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `body` text DEFAULT NULL,
  `author_username` varchar(255) NOT NULL,
  `device_name` varchar(255) NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `surname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `name`, `surname`, `email`, `role`, `created_at`) VALUES
(1, 'paco', 'scrypt:32768:8:1$bwB6e27o61TO6Ldq$8f9c838015fcf3f9767eea96c66a68477b3daf61f088279dcedc574cd6740fa3cdfeca090974c19bb484dca452829fa81cb317f9c3e30d453d68f8077bbb09ae', 'Paco', 'De La Oz', 'vdelgado@paratytech.com', 'admin', '2025-05-22 17:56:37'),
(2, 'lola', 'scrypt:32768:8:1$fjpkI1nWLqKm25RY$ced468059cbb9c1223218a8e5d0623ee60e27a149d1a2a799ad41a440081febbdc64f3254ef085b49ea22d26b4833664cb33909b6d5b2f13a48bb1025604fac9', 'Lola', 'Añil', 'email@email.es', 'user', '2025-05-25 09:04:59');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `components`
--
ALTER TABLE `components`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `configurations`
--
ALTER TABLE `configurations`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `devices`
--
ALTER TABLE `devices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `peripherals`
--
ALTER TABLE `peripherals`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`id`),
  ADD KEY `author_username` (`author_username`),
  ADD KEY `device_name` (`device_name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `components`
--
ALTER TABLE `components`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=248;

--
-- AUTO_INCREMENT for table `devices`
--
ALTER TABLE `devices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=622;

--
-- AUTO_INCREMENT for table `peripherals`
--
ALTER TABLE `peripherals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`author_username`) REFERENCES `users` (`username`),
  ADD CONSTRAINT `reports_ibfk_2` FOREIGN KEY (`device_name`) REFERENCES `devices` (`name`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
