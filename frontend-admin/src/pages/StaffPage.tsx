import React, { useState } from 'react';
import { Plus, Trash2 } from 'lucide-react';

export function StaffPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  // Mock Data for V0
  const [staff, setStaff] = useState([
    { id: 1, name: 'John Doe', role: 'MANAGER', pin: '****' },
    { id: 2, name: 'Jane Smith', role: 'WAITER', pin: '****' },
  ]);
  // TODO: Use setStaff when API is connected
  console.log(setStaff);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Staff Management</h1>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-indigo-600 text-white px-4 py-2 rounded-md flex items-center hover:bg-indigo-700"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Staff
        </button>
      </div>

      <div className="bg-white shadow rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">PIN</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {staff.map((member) => (
              <tr key={member.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{member.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    member.role === 'MANAGER' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {member.role}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">****</td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-red-600 hover:text-red-900">
                    <Trash2 className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Simple Modal Placeholder */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div className="bg-white p-6 rounded-lg shadow-lg w-96">
                <h2 className="text-xl font-bold mb-4">Add Staff Member</h2>
                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Name</label>
                        <input type="text" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" placeholder="e.g. Alice" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">PIN (4-6 digits)</label>
                        <input type="password" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" placeholder="1234" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Role</label>
                        <select className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
                            <option>WAITER</option>
                            <option>MANAGER</option>
                        </select>
                    </div>
                    <div className="flex justify-end space-x-2 mt-4">
                        <button onClick={() => setIsModalOpen(false)} className="px-4 py-2 bg-gray-200 rounded">Cancel</button>
                        <button className="px-4 py-2 bg-indigo-600 text-white rounded">Save</button>
                    </div>
                </div>
            </div>
        </div>
      )}
    </div>
  );
}
