import React, { useEffect, useState } from 'react';
import $ from 'jquery';
// import 'datatables.net-dt/css/jquery.dataTables.min.css';
import 'datatables.net';

function App() {
  const [birth_date, setbirth_date] = useState('');
  const [income, setIncome] = useState('');
  const [age, setage] = useState('');
  const[annual_interest_rate, setannual_interest_rate] = useState('');
  const [tableData, setTableData] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/get-portfolio-trajectory/')
      .then(response => response.json())
      .then(data => {
        setTableData(data);
        $('#myTable').DataTable();
      });
  }, []);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/default-values/')
      .then(response => response.json())
      .then(data => {
        setbirth_date(data.birth_year);
        setIncome(data.income);
        setage(data.retirement_age);
        setannual_interest_rate(data.annual_interest_rate);
      });
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission here
   const data = { age: age,
    annual_interest_rate: annual_interest_rate,
    income: income,
    birth_date: birth_date
   };
    fetch('http://127.0.0.1:8000/monthly-retirement-fund/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    };

  return (
<div className="App">
  <header className="App-header">
    <h1>Retirement Portfolio</h1>
  </header>
  <div className='left-panel'>
  <main>
    <form onSubmit={handleSubmit}>
      <div className="form-row">
        <label>Select Your Birth Date:</label>
        <input type="date" defaultValue={birth_date} />
      </div>
      <div className="form-row">
        <label>Annual Income:</label>
          <input type="range" min="0" max="2000000" value={income} onChange={e => setIncome(e.target.value)} />
          <span>{income}</span>
      </div>
      <div className="form-row">
        <label>Expected Retirement Age:</label>
        <input type="number" value={age} onChange={e => setage(e.target.value)} />
      </div>
      <div className="form-row">
        <label>Annual Rate of Interest:</label>
        <input type="range" min="0" max="20" value={annual_interest_rate} onChange={e => setannual_interest_rate(e.target.value)} />
        <span>{annual_interest_rate}%</span>
      </div>
      <div className='form-row'>
        <label><button type="submit">Calculate</button></label>
      </div>
    </form>
  </main>
  </div>
  <div className="right-panel">
        <div className="row">

        <table id="myTable" className="display">
        <thead>
          <tr>
            <th>Age</th>
            <th>Year</th>
            <th>Rate Of Return</th>
            <th>Inflation Rate</th>
            <th>Investment @ Begin</th>
            <th>Investment @ end</th>
            <th>Net Gain</th>
            <th>Inflation Adjusted Rate</th>
            <th>Real Growth</th>
          </tr>
        </thead>
        <tbody>
          {tableData.map((item, index) => (
            <tr key={index}>
              <td>{item.age}</td>
              <td>{item.year}</td>
              <td>{item.rate_of_return}</td>
              <td>{item.inflation_rate}</td>
              <td>{item.inv_begin}</td>
              <td>{item.inv_end}</td>
              <td>{item.net_gain}</td>
              <td>{item.inflation_adj_rate}</td>
              <td>{item.real_growth}</td>
            </tr>
          ))}
        </tbody>
      </table>


        </div>
        <div className="row">Row 2</div>
    </div>
</div>
  );
}

export default App;