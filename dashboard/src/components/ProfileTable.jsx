import React, { useEffect, useState } from "react";
import axios from "axios";

const ProfileTable = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/profile_result")
      .then(res => setData(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>Table</th>
          <th>Column</th>
          <th>Null %</th>
          <th>Distinct</th>
          <th>Duplicates</th>
          <th>Min</th>
          <th>Max</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row, idx) => (
          <tr key={idx}>
            <td>{row.table_name}</td>
            <td>{row.column_name}</td>
            <td>{row.null_percentage}</td>
            <td>{row.distinct_count}</td>
            <td>{row.duplicate_count}</td>
            <td>{row.min_value}</td>
            <td>{row.max_value}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default ProfileTable;
