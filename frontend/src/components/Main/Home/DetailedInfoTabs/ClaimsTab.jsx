import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ClaimsTab() {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    failureNode: '',
    restorationMethod: '',
    serviceCompany: '',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/api/claims/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        console.log('Fetched data:', response.data);
        const sortedData = response.data.sort((a, b) => new Date(a.failure_date) - new Date(b.failure_date));
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
        const matchesFailureNode = filters.failureNode === '' || item.failure_node === filters.failureNode;
        const matchesRestorationMethod = filters.restorationMethod === '' || item.restoration_method === filters.restorationMethod;
        const matchesServiceCompany = filters.serviceCompany === '' || item.service_companies.some(company => company.last_name === filters.serviceCompany);
        return matchesFailureNode && matchesRestorationMethod && matchesServiceCompany;
      });
      setFilteredData(filtered);
    };
    applyFilters();
  }, [filters, data]);

  const renderCell = (value) => {
    return value !== undefined && value !== null ? value : '-----';
  };

  const renderRow = (item) => {
    return (
      <tr key={item.id}>
        <td>{renderCell(item.serial_number)}</td>
        <td>{renderCell(item.failure_date)}</td>
        <td>{renderCell(item.operating_hours)}</td>
        <td>{renderCell(item.failure_node)}</td>
        <td>{renderCell(item.failure_description)}</td>
        <td>{renderCell(item.restoration_method)}</td>
        <td>{renderCell(item.spare_parts_used)}</td>
        <td>{renderCell(item.restoration_date)}</td>
        <td>{renderCell(item.downtime)}</td>
      </tr>
    );
  };

  return (
    <>
      <h1 className="tech-info-header">Информация о рекламациях по Вашей технике</h1>
      <div className="filter-container">
        <label>
          Узел отказа:
          <select className="select-label" name="failureNode" value={filters.failureNode} onChange={handleFilterChange}>
            <option value="">Все</option>
            {Array.from(new Set(data.map(item => item.failure_node))).map((node, index) => (
              <option key={index} value={node}>{node}</option>
            ))}
          </select>
        </label>
        <label>
          Способ восстановления:
          <select className="select-label" name="restorationMethod" value={filters.restorationMethod} onChange={handleFilterChange}>
            <option value="">Все</option>
            {Array.from(new Set(data.map(item => item.restoration_method))).map((method, index) => (
              <option key={index} value={method}>{method}</option>
            ))}
          </select>
        </label>
        <label>
          Сервисная компания:
          <select className="select-label" name="serviceCompany" value={filters.serviceCompany} onChange={handleFilterChange}>
            <option value="">Все</option>
            {Array.from(new Set(data.flatMap(item => item.service_companies.map(company => company.last_name)))).map((company, index) => (
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
                <th>Дата отказа</th>
                <th>Наработка, м/час</th>
                <th>Узел отказа</th>
                <th>Описание отказа</th>
                <th>Способ восстановления</th>
                <th>Используемые запасные части</th>
                <th>Дата восстановления</th>
                <th>Время простоя техники</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.map((item) => renderRow(item))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}

export default ClaimsTab;




