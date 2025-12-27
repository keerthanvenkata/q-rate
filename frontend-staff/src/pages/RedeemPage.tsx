import React, { useState } from 'react';

export const RedeemPage: React.FC = () => {
    const [code, setCode] = useState('');

    const handleRedeem = (e: React.FormEvent) => {
        e.preventDefault();
        alert(`Redeeming: ${code} (Not implemented in V0 prototype yet)`);
    };

    return (
        <div className="card">
            <h2>Redeem Coupon</h2>
            <p className="text-muted mb-4">Enter the code from the customer's phone.</p>
            
            <form onSubmit={handleRedeem}>
                <div className="form-group">
                    <label className="label">Coupon Code</label>
                    <input 
                        className="input" 
                        placeholder="LATTE-492" 
                        value={code} 
                        onChange={(e) => setCode(e.target.value.toUpperCase())}
                        required
                    />
                </div>
                <button className="btn btn-primary" type="submit">Verify & Redeem</button>
            </form>
        </div>
    );
};
