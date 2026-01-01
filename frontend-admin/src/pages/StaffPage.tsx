import { useState } from 'react';
import { Plus, Trash2 } from 'lucide-react';
import { adminService } from '../services/api';
import type { Staff } from '../services/api';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function StaffPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const queryClient = useQueryClient();
  
  // Fetch Staff from API
  const { data: staff, isLoading } = useQuery({
    queryKey: ['staff'],
    queryFn: adminService.getStaff,
  });

  // Create Staff Mutation
  const createMutation = useMutation({
    mutationFn: adminService.createStaff,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff'] });
      setIsModalOpen(false);
      setFormData({ name: '', pin: '', role: 'waiter' });
    }
  });

  // Delete Staff Mutation
  const deleteMutation = useMutation({
    mutationFn: adminService.deleteStaff,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff'] });
    }
  });

  // Form State
  const [formData, setFormData] = useState<{
    name: string;
    pin: string;
    role: 'manager' | 'waiter';
  }>({ name: '', pin: '', role: 'waiter' });

  const handleSubmit = () => {
    createMutation.mutate({
      ...formData,
      cafe_id: 1 // V0 Mock ID
    });
  };

  if (isLoading) return <div className="p-8 text-center text-gray-500">Loading staff data...</div>;

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
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {staff?.map((member: Staff) => (
              <tr key={member.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{member.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    member.role === 'manager' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {member.role}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span className="text-green-600">Active</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button 
                    onClick={() => deleteMutation.mutate(member.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            ))}
            {staff?.length === 0 && (
                <tr>
                    <td colSpan={4} className="px-6 py-4 text-center text-gray-500">No staff members found. Add one to get started.</td>
                </tr>
            )}
          </tbody>
        </table>
      </div>
      
      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded-lg shadow-lg w-96">
                <h2 className="text-xl font-bold mb-4">Add Staff Member</h2>
                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Name</label>
                        <input 
                            type="text" 
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" 
                            placeholder="e.g. Alice"
                            value={formData.name}
                            onChange={(e) => setFormData({...formData, name: e.target.value})}    
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">PIN (4-6 digits)</label>
                        <input 
                            type="password" 
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" 
                            placeholder="1234"
                            value={formData.pin}
                            onChange={(e) => setFormData({...formData, pin: e.target.value})}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Role</label>
                        <select 
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                            value={formData.role}
                            onChange={(e) => setFormData({...formData, role: e.target.value as 'manager' | 'waiter'})}
                        >
                            <option value="waiter">WAITER</option>
                            <option value="manager">MANAGER</option>
                        </select>
                    </div>
                    <div className="flex justify-end space-x-2 mt-4">
                        <button onClick={() => setIsModalOpen(false)} className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">Cancel</button>
                        <button 
                            onClick={handleSubmit} 
                            disabled={createMutation.isPending}
                            className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 disabled:opacity-50"
                        >
                            {createMutation.isPending ? 'Saving...' : 'Save'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
      )}
    </div>
  );
}
