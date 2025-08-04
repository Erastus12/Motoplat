-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 16, 2025 at 06:23 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `data_plat_motor`
--

-- --------------------------------------------------------

--
-- Table structure for table `data_plat`
--

CREATE TABLE `data_plat` (
  `id` int(11) NOT NULL,
  `nomor_polisi` varchar(16) NOT NULL,
  `merk` varchar(25) NOT NULL,
  `model` varchar(100) NOT NULL,
  `warna` varchar(25) NOT NULL,
  `tahun` int(10) NOT NULL,
  `akhir_pajak` date NOT NULL,
  `akhir_stnk` date NOT NULL,
  `pelanggaran` varchar(255) NOT NULL,
  `status` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `data_plat`
--

INSERT INTO `data_plat` (`id`, `nomor_polisi`, `merk`, `model`, `warna`, `tahun`, `akhir_pajak`, `akhir_stnk`, `pelanggaran`, `status`) VALUES
(1, 'B 3499 EFW', 'HONDA', 'BEAT', 'hitam', 2022, '2027-07-07', '2028-08-08', 'Tidak ada', 'Tidak Melanggar'),
(2, 'BK 1332 ADE', 'YAMAHA', 'NMAX TURBO', 'Hitam', 2019, '2029-05-17', '2029-07-20', 'Tidak Ada', 'Tidak Melanggar'),
(3, 'BK 5787 SAJ', 'HONDA', 'BeAT Sreet', 'HITAM', 2021, '2025-05-07', '2025-10-05', 'Belum bayar denda pelanggaran', 'Melanggar');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `data_plat`
--
ALTER TABLE `data_plat`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `data_plat`
--
ALTER TABLE `data_plat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
