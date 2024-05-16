import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MaintenanceTab() {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    maintenanceType: '',
    serialNumber: '',
    serviceCompany: '',
  });
  const [selectedSerialNumber, setSelectedSerialNumber] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/api/maintenance/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const sortedData = response.data.sort((a, b) => new Date(a.date_performed) - new Date(b.date_performed));
        setData(sortedData);
        setFilteredData(sortedData);
      } catch (error) {
        if (error.response && error.response.status === 403) {
          setError('Forbidden');
        } else {
          setError('An error occurred while fetching data.');
        }
      }
    };
    fetchData();
  }, []);

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value,
    });
  };

  useEffect(() => {
    const applyFilters = () => {
      const filtered = data.filter(item => {
        const matchesMaintenanceType = filters.maintenanceType === '' || item.maintenance_type_name === filters.maintenanceType;
        const matchesSerialNumber = filters.serialNumber === '' || item.machine_serial_number === filters.serialNumber;
        const matchesServiceCompany = filters.serviceCompany === '' || item.performing_organization_name === filters.serviceCompany;
        return matchesMaintenanceType && matchesSerialNumber && matchesServiceCompany;
      });
      setFilteredData(filtered);
    };
    applyFilters();
  }, [filters, data]);

  const handleSerialNumberClick = (serialNumber) => {
    setSelectedSerialNumber(serialNumber);
    setFilters({
      ...filters,
      serialNumber: serialNumber,
    });
  };

  const handleBackClick = () => {
    setSelectedSerialNumber(null);
    setFilters({
      ...filters,
      serialNumber: '',
    });
  };

  const renderCell = (value) => {
    return value !== undefined && value !== null ? value : '-----';
  };

  const renderRow = (item, index) => {
    return (
      <tr key={index}>
        <td>
          <a href="#!" className="link-button" onClick={() => handleSerialNumberClick(item.machine_serial_number)}>
            {renderCell(item.machine_serial_number)}
          </a>
        </td>
        <td>{renderCell(item.maintenance_type_name)}</td>
        <td>{renderCell(item.date_performed)}</td>
        <td>{renderCell(item.hours_worked)}</td>
        <td>{renderCell(item.order_number)}</td>
        <td>{renderCell(item.order_date)}</td>
        <td>{renderCell(item.performing_organization_name)}</td>
      </tr>
    );
  };

  return (
    <>
      <h1 className="tech-info-header">Информация о проведенных ТО Вашей техники</h1>
      {selectedSerialNumber && (
        <h2 className="machine-info">Машина с заводским номером: {selectedSerialNumber}</h2>
      )}
      <div className="filter-container">
        <label className="label">
          Вид ТО:
          <select className="select-label" name="maintenanceType" value={filters.maintenanceType} onChange={handleFilterChange}>
            <option value="">Все</option>
            {Array.from(new Set(data.map(item => item.maintenance_type_name))).map((type, index) => (
              <option key={index} value={type}>{type}</option>
            ))}
          </select>
        </label>
        <label className="label">
          Зав. номер машины:
          <select className="select-label" name="serialNumber" value={filters.serialNumber} onChange={handleFilterChange}>
            <option value="">Все</option>
            {Array.from(new Set(data.map(item => item.machine_serial_number))).map((serial, index) => (
              <option key={index} value={serial}>{serial}</option>
            ))}
          </select>
        </label>
        <label className="label">
          Сервисная компания:
          <select className="select-label" name="serviceCompany" value={filters.serviceCompany} onChange={handleFilterChange}>
            <option value="">Все</option>
            {Array.from(new Set(data.map(item => item.performing_organization_name))).map((company, index) => (
              <option key={index} value={company}>{company}</option>
            ))}
          </select>
        </label>
      </div>
      <div className="table-container">
        {error ? (
          <p>{error}</p>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Зав. № машины</th>
                <th>Вид ТО</th>
                <th>Дата проведения ТО</th>
                <th>Наработка, м/час</th>
                <th>№ заказ-наряда</th>
                <th>Дата заказ-наряда</th>
                <th>Организация, проводившая ТО</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.map((item, index) => renderRow(item, index))}
            </tbody>
          </table>
        )}
      </div>
      {selectedSerialNumber && (
        <button className="reset-button" onClick={handleBackClick}>Назад</button>
      )}
    </>
  );
}

export default MaintenanceTab;




