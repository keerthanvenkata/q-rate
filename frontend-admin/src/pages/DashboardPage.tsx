import React from 'react';

export function DashboardPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-500">Visits Today</h3>
          <p className="mt-2 text-3xl font-bold text-gray-900">24</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
           <h3 className="text-sm font-medium text-gray-500">Check-ins Today</h3>
           <p className="mt-2 text-3xl font-bold text-indigo-600">18</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
           <h3 className="text-sm font-medium text-gray-500">Redemptions</h3>
           <p className="mt-2 text-3xl font-bold text-green-600">2</p>
        </div>
      </div>
    </div>
  );
}
