import React from 'react';
import { StaffInputForm } from '../components/StaffInputForm';

export const VisitPage: React.FC = () => {
    return (
        <div>
            <h2 className="mb-4">New Visit</h2>
            <StaffInputForm />
        </div>
    );
};
