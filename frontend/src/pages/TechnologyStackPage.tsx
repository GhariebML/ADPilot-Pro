import React from 'react';
import { TechnologyStackView } from '../components/TechnologyStackView';

export const TechnologyStackPage: React.FC = () => {
  return (
    <div className="w-full min-h-screen bg-[#07090e] p-6 lg:p-8">
      <div className="max-w-7xl mx-auto">
        <TechnologyStackView />
      </div>
    </div>
  );
};

export default TechnologyStackPage;
