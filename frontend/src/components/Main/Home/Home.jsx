import React from 'react';
import { useAuth } from '../../../context/AuthContext';
import BasicInfoTable from './BasicInfoTable/BasicInfoTable';
import DetailedInfoTabs from './DetailedInfoTabs/DetailedInfoTabs';
import './Home.css';

function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="home">
      {isAuthenticated ? <DetailedInfoTabs /> : <BasicInfoTable />}
    </div>
  );
}

export default Home;