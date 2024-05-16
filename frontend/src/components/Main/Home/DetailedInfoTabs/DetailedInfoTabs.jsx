import React, { useState, useEffect, useCallback } from 'react';
import { Tabs, Tab } from 'react-bootstrap';
import GeneralInfoTab from './GeneralInfoTab';
import MaintenanceTab from './MaintenanceTab';
import ClaimsTab from './ClaimsTab';
import { useAuth } from '../../../../context/AuthContext';
import axios from 'axios';
import './DetailedInfoTabs.css';

function DetailedInfoTabs() {
    const { user, loading, logout, checkAuthStatus } = useAuth();
    const [key, setKey] = useState('general');
    const [authChecked, setAuthChecked] = useState(false);

    const verifyAuthStatus = useCallback(async () => {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const response = await axios.get('http://localhost:8000/accounts/check_auth_status/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (!response.data.is_authenticated) {
                    logout();
                } else {
                    setAuthChecked(true);
                }
            } catch (error) {
                console.error('Error checking auth status:', error);
                logout();
            }
        }
    }, [logout]);

    useEffect(() => {
        verifyAuthStatus();
    }, [verifyAuthStatus]);

    useEffect(() => {
        if (!loading && !authChecked) {
            verifyAuthStatus();
        }
    }, [loading, authChecked, verifyAuthStatus]);

    useEffect(() => {
        console.log('User:', user);
    }, [user]);

    const displayUserInfo = () => {
        if (loading) return 'Загрузка данных...';
        if (!user) return '';

        let displayInfo = user.last_name || 'Недоступно';
        if (user.is_client && user.service_companies) {
            const serviceCompaniesDisplay = user.service_companies.join(', ');
            displayInfo += ` / Сервисная компания ${serviceCompaniesDisplay}`;
        }
        return displayInfo;
    };

    return (
        <div className="detailed-info-tabs-container">
            <h2 className="user-info">{displayUserInfo()}</h2>
            <Tabs
                id="detailed-info-tabs"
                className="custom-tabs"
                activeKey={key}
                onSelect={(k) => {
                    checkAuthStatus();  // Проверка авторизации при переключении вкладок
                    setKey(k);
                }}
            >
                <Tab eventKey="general" title="Общая информация">
                    {key === 'general' && <GeneralInfoTab />}
                </Tab>
                <Tab eventKey="maintenance" title="ТО">
                    {key === 'maintenance' && <MaintenanceTab />}
                </Tab>
                <Tab eventKey="claims" title="Рекламации">
                    {key === 'claims' && <ClaimsTab />}
                </Tab>
            </Tabs>
        </div>
    );
}

export default DetailedInfoTabs;







