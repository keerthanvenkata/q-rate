import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { visitsApi } from '../api/visits';
import type { CreateVisitRequest } from '../api/visits';
import { Loader2, CheckCircle, Plus, Minus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const StaffInputForm: React.FC = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState<CreateVisitRequest>({
        phone_number: '',
        bill_id: '',
        bill_amount: 0,
        verbal_consent: false,
        customer_name: '',
        guest_count: 1 // Default self
    });

    const mutation = useMutation({
        mutationFn: visitsApi.create,
        onSuccess: () => {
             // Show success state then redirect or clear
             alert("Visit Logged! WhatsApp sent.");
             navigate('/');
        },
        onError: (error) => {
            alert("Failed to log visit: " + error);
        }
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : 
                    name === 'bill_amount' ? parseFloat(value) : value
        }));
    };

    const adjustGuests = (delta: number) => {
        setFormData(prev => ({
            ...prev,
            guest_count: Math.max(1, prev.guest_count + delta)
        }));
    };

    return (
        <form onSubmit={(e) => { e.preventDefault(); mutation.mutate(formData); }} className="card">
            
            {/* Phone */}
            <div className="form-group">
                <label className="label">Customer Phone *</label>
                <input 
                    className="input"
                    name="phone_number"
                    type="tel"
                    placeholder="9876543210"
                    required
                    value={formData.phone_number}
                    onChange={handleChange}
                />
            </div>

            {/* Bill Details */}
            <div className="form-group" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                     <label className="label">Bill ID *</label>
                     <input className="input" name="bill_id" required value={formData.bill_id} onChange={handleChange} />
                </div>
                <div>
                     <label className="label">Amount (₹) *</label>
                     <input className="input" name="bill_amount" type="number" step="0.01" required value={formData.bill_amount} onChange={handleChange} />
                </div>
            </div>

            {/* Guest Count (Referral Bonus) */}
            <div className="form-group">
                <label className="label">Total Guests (Referral Bonus)</label>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <button type="button" className="btn-outline" style={{width: '40px'}} onClick={() => adjustGuests(-1)}><Minus size={16}/></button>
                    <span style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>{formData.guest_count}</span>
                    <button type="button" className="btn-outline" style={{width: '40px'}} onClick={() => adjustGuests(1)}><Plus size={16}/></button>
                </div>
            </div>

            {/* Consent */}
            <div className="form-group">
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                    <input 
                        type="checkbox" 
                        name="verbal_consent" 
                        required 
                        checked={formData.verbal_consent}
                        onChange={handleChange}
                        style={{ width: '1.25rem', height: '1.25rem' }}
                    />
                    <span>I explained the review process.</span>
                </label>
            </div>

            <button type="submit" className="btn btn-primary" disabled={!formData.verbal_consent || mutation.isPending}>
                {mutation.isPending ? <Loader2 className="animate-spin" /> : <CheckCircle />}
                {mutation.isPending ? 'Sending...' : 'Send Magic Link'}
            </button>

        </form>
    );
};
