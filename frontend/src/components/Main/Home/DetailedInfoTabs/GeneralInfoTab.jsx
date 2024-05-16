import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function GeneralInfoTab() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    model: '',
    engineModel: '',
    transmissionModel: '',
    drivingAxleModel: '',
    steeringAxleModel: '',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/api/machine_details/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        const withDates = response.data.filter(item => item.shipment_date && item.shipment_date !== '-----');
        const withoutDates = response.data.filter(item => !item.shipment_date || item.shipment_date === '-----');
        const sortedWithDates = withDates.sort((a, b) => new Date(a.shipment_date) - new Date(b.shipment_date));
        const sortedData = [...sortedWithDates, ...withoutDates];

        setData(sortedData);
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

  const applyFilters = (items) => {
    return items.filter(item => {
      return (
        (filters.model === '' || item.model_name === filters.model) &&
        (filters.engineModel === '' || item.engine_model_name === filters.engineModel) &&
        (filters.transmissionModel === '' || item.transmission_model_name === filters.transmissionModel) &&
        (filters.drivingAxleModel === '' || item.driving_axle_model_name === filters.drivingAxleModel) &&
        (filters.steeringAxleModel === '' || item.steering_axle_model_name === filters.steeringAxleModel)
      );
    });
  };

  const renderCell = (value) => {
    return value !== undefined && value !== null ? value : '-----';
  };

  return (
    <>
      <h1 className="tech-info-header">Информация о комплектации и технических характеристиках Вашей техники</h1>
      <div className="filter-container">
        <label>
          Модель техники:
          <select name="model" value={filters.model} onChange={handleFilterChange}>
            <option value="">Все</option>
            {Array.from(new Set(data.map(item => item.model_name))).map((model, index) => (
              <option key={index} value={model}>{model}</option>
            ))}
          </select>
        </label>
        <label>
          Модель двигателя:
          <select name="engineModel" value={filters.engineModel} onChange={handleFilterChange}>
            <option value="">Все</option>
            {Array.from(new Set(data.map(item => item.engine_model_name))).map((engineModel, index) => (
              <option key={index} value={engineModel}>{engineModel}</option>
            ))}
          </select>
        </label>
        <label>
          Модель трансмиссии:
          <select name="transmissionModel" value={filters.transmissionModel} onChange={handleFilterChange}>
            <option value="">Все</option>
            {Array.from(new Set(data.map(item => item.transmission_model_name))).map((transmissionModel, index) => (
              <option key={index} value={transmissionModel}>{transmissionModel}</option>
            ))}
          </select>
        </label>
        <label>
          Модель ведущего моста:
          <select name="drivingAxleModel" value={filters.drivingAxleModel} onChange={handleFilterChange}>
            <option value="">Все</option>
            {Array.from(new Set(data.map(item => item.driving_axle_model_name))).map((drivingAxleModel, index) => (
              <option key={index} value={drivingAxleModel}>{drivingAxleModel}</option>
            ))}
          </select>
        </label>
        <label>
          Модель управляемого моста:
          <select name="steeringAxleModel" value={filters.steeringAxleModel} onChange={handleFilterChange}>
            <option value="">Все</option>
            {Array.from(new Set(data.map(item => item.steering_axle_model_name))).map((steeringAxleModel, index) => (
              <option key={index} value={steeringAxleModel}>{steeringAxleModel}</option>
            ))}
          </select>
        </label>
      </div>
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Зав. № машины</th>
              <th>Модель техники</th>
              <th>Модель двигателя</th>
              <th>Зав. № двигателя</th>
              <th>Модель трансмиссии</th>
              <th>Зав. № трансмиссии</th>
              <th>Модель ведущего моста</th>
              <th>Зав. № ведущего моста</th>
              <th>Модель управляемого моста</th>
              <th>Зав. № управляемого моста</th>
              <th>Дата отгрузки с завода</th>
              <th>Покупатель</th>
              <th>Грузополучатель</th>
              <th>Адрес поставки</th>
              <th>Комплектация</th>
              <th>Сервисная компания</th>
            </tr>
          </thead>
          <tbody>
            {applyFilters(data).map((item, index) => (
              <tr key={index}>
                <td>{renderCell(item.serial_number)}</td>
                <td><Link to={`/reference/Модель%20техники/${item.model_name}`}>{item.model_name}</Link></td>
                <td><Link to={`/reference/Модель%20двигателя/${item.engine_model_name}`}>{item.engine_model_name}</Link></td>
                <td>{renderCell(item.engine_serial_number)}</td>
                <td><Link to={`/reference/Модель%20трансмиссии/${item.transmission_model_name}`}>{item.transmission_model_name}</Link></td>
                <td>{renderCell(item.transmission_serial_number)}</td>
                <td><Link to={`/reference/Модель%20ведущего%20моста/${item.driving_axle_model_name}`}>{item.driving_axle_model_name}</Link></td>
                <td>{renderCell(item.driving_axle_serial_number)}</td>
                <td><Link to={`/reference/Модель%20управляемого%20моста/${item.steering_axle_model_name}`}>{item.steering_axle_model_name}</Link></td>
                <td>{renderCell(item.steering_axle_serial_number)}</td>
                <td>{renderCell(item.shipment_date)}</td>
                <td>{renderCell(item.client)}</td>
                <td>{renderCell(item.consignee)}</td>
                <td>{renderCell(item.operation_address)}</td>
                <td>{renderCell(item.configuration)}</td>
                <td>{renderCell(item.service_companies?.join(', '))}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

export default GeneralInfoTab;







