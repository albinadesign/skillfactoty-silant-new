import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Reference.css';

function Reference() {
    const { directoryName, name } = useParams();
    const [description, setDescription] = useState("");
    const navigate = useNavigate();
  
    useEffect(() => {
        const fetchData = async () => {
            const encodedDirectoryName = encodeURIComponent(directoryName);
            const encodedName = encodeURIComponent(name);
            const url = `http://localhost:8000/api/references/${encodedDirectoryName}/${encodedName}`;
            try {
                const response = await axios.get(url);
                console.log("Полученные данные:", response.data);
                const matchedReference = response.data.find(ref => ref.name === name && ref.directory_name === directoryName);
                if (matchedReference) {
                    setDescription(matchedReference.description || "Описание отсутствует");
                } else {
                    setDescription("Описание отсутствует");
                }
            } catch (error) {
                console.error('Ошибка при получении данных о справочнике:', error);
                if (error.response && error.response.status === 403) {
                    console.log('Доступ запрещён, перенаправление на страницу входа');
                    navigate('/login');
                }
            }
        };
    
        fetchData();
    }, [directoryName, name, navigate]);
  
    const handleBack = () => {
      navigate(-1);
    };
  
    return (
      <div className="reference">
        <h1 className="reference-header">{`${directoryName} ${name}`}</h1>
        <div className="reference-description">{description}
        {description.trim() ? description : "Описание отсутствует"}
        </div>
        <button className="reference-back-button" onClick={handleBack}>Назад</button>
      </div>
    );
  }
  
  export default Reference;