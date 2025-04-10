import os
import json
from datetime import datetime
import base64

def generate_html_report(domain, results, output_dir="results"):
    """
    Generate an interactive HTML report from the scoring results.
    
    Args:
        domain (str): The target domain
        results (dict): The scoring results
        output_dir (str): The directory to save the report to
        
    Returns:
        str: The path to the saved HTML report
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create the output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{domain}_{timestamp}_report.html"
    filepath = os.path.join(output_dir, filename)
    
    # Calculate statistics for the report
    total_subdomains = len(results.get('scored_subdomains', []))
    high_risk = sum(1 for item in results.get('scored_subdomains', []) if item.get('score', 0) >= 8)
    medium_risk = sum(1 for item in results.get('scored_subdomains', []) if 5 <= item.get('score', 0) < 8)
    low_risk = sum(1 for item in results.get('scored_subdomains', []) if 1 <= item.get('score', 0) < 5)
    
    # Calculate average score
    avg_score = 0
    if total_subdomains > 0:
        avg_score = sum(item.get('score', 0) for item in results.get('scored_subdomains', [])) / total_subdomains
    
    # Current date and time
    scan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_year = datetime.now().year
    
    # Sort subdomains by score (high to low)
    sorted_subdomains = sorted(results.get('scored_subdomains', []), key=lambda x: x.get('score', 0), reverse=True)
    
    # Generate table rows for each subdomain
    table_rows = ""
    for item in sorted_subdomains:
        score = item.get('score', 0)
        
        # Determine risk level and color
        risk_level = "High" if score >= 8 else "Medium" if score >= 5 else "Low"
        risk_class = "risk-high" if score >= 8 else "risk-medium" if score >= 5 else "risk-low"
        color = "#ff4d4d" if score >= 8 else "#ffa64d" if score >= 5 else "#4dbd74"
        
        table_rows += f"""
        <tr>
            <td>{item['subdomain']}</td>
            <td>
                <div>{score}/10</div>
                <div class="score-bar">
                    <div class="score-value" style="width: {score*10}%; background-color: {color};"></div>
                </div>
            </td>
            <td>
                <div class="risk-badge {risk_class}">
                    {risk_level}
                </div>
            </td>
            <td>{item['reason']}</td>
        </tr>
        """
    
    # Generate the JSON data for the raw view
    json_data = json.dumps(results, indent=4)
    
    # Generate the HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartSubAI Report - {domain}</title>
    <style>
        :root {{
            --primary-color: #4a6fa5;
            --secondary-color: #336699;
            --accent-color: #5d93d6;
            --background-color: #f5f7fa;
            --card-bg-color: #ffffff;
            --text-color: #333333;
            --light-text: #666666;
            --high-risk: #ff4d4d;
            --medium-risk: #ffa64d;
            --low-risk: #4dbd74;
            --header-height: 60px;
            --sidebar-width: 280px;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        body {{
            background-color: var(--background-color);
            color: var(--text-color);
            line-height: 1.6;
        }}
        
        .container {{
            display: flex;
            min-height: 100vh;
        }}
        
        .sidebar {{
            width: var(--sidebar-width);
            background-color: var(--primary-color);
            color: #fff;
            padding: 20px;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }}
        
        .sidebar h1 {{
            font-size: 24px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .sidebar-section {{
            margin-bottom: 20px;
        }}
        
        .sidebar-section h2 {{
            font-size: 18px;
            margin-bottom: 10px;
        }}
        
        .sidebar-section p {{
            font-size: 14px;
            margin-bottom: 6px;
        }}
        
        .main-content {{
            flex: 1;
            margin-left: var(--sidebar-width);
            padding: 20px;
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eaeaea;
        }}
        
        .domain-title {{
            font-size: 28px;
            color: var(--secondary-color);
        }}
        
        .scan-info {{
            color: var(--light-text);
            font-size: 14px;
        }}
        
        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .dashboard-card {{
            background-color: var(--card-bg-color);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            text-align: center;
        }}
        
        .dashboard-card h2 {{
            font-size: 16px;
            margin-bottom: 10px;
            color: var(--light-text);
        }}
        
        .dashboard-card .value {{
            font-size: 36px;
            font-weight: bold;
            color: var(--primary-color);
        }}
        
        .card {{
            background-color: var(--card-bg-color);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }}
        
        .card h2 {{
            font-size: 20px;
            margin-bottom: 20px;
            color: var(--secondary-color);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        table th, table td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eaeaea;
        }}
        
        table th {{
            background-color: var(--primary-color);
            color: #fff;
            font-weight: 600;
            position: sticky;
            top: 0;
        }}
        
        table tr:hover {{
            background-color: rgba(93, 147, 214, 0.1);
        }}
        
        .risk-badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            color: #fff;
            text-align: center;
            min-width: 80px;
        }}
        
        .risk-high {{
            background-color: var(--high-risk);
        }}
        
        .risk-medium {{
            background-color: var(--medium-risk);
        }}
        
        .risk-low {{
            background-color: var(--low-risk);
        }}
        
        .score-bar {{
            height: 8px;
            background-color: #e0e0e0;
            border-radius: 4px;
            margin-top: 5px;
            overflow: hidden;
        }}
        
        .score-value {{
            height: 100%;
            border-radius: 4px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: var(--light-text);
            font-size: 14px;
        }}
        
        .collapsible {{
            background-color: var(--primary-color);
            color: white;
            cursor: pointer;
            padding: 18px;
            width: 100%;
            border: none;
            text-align: left;
            outline: none;
            font-size: 16px;
            border-radius: 5px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .active, .collapsible:hover {{
            background-color: var(--accent-color);
        }}
        
        .content {{
            padding: 0 18px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.2s ease-out;
            background-color: var(--card-bg-color);
            border-radius: 0 0 5px 5px;
            margin-bottom: 20px;
        }}
        
        #jsonData {{
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: monospace;
            white-space: pre;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                flex-direction: column;
            }}
            
            .sidebar {{
                width: 100%;
                height: auto;
                position: relative;
            }}
            
            .main-content {{
                margin-left: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h1>SmartSubAI</h1>
            <div class="sidebar-section">
                <h2>Scan Information</h2>
                <p><strong>Domain:</strong> {domain}</p>
                <p><strong>Scan Date:</strong> {scan_time}</p>
                <p><strong>Total Subdomains:</strong> {total_subdomains}</p>
            </div>
            <div class="sidebar-section">
                <h2>Risk Summary</h2>
                <p><strong>High Risk (8-10):</strong> {high_risk}</p>
                <p><strong>Medium Risk (5-7):</strong> {medium_risk}</p>
                <p><strong>Low Risk (1-4):</strong> {low_risk}</p>
            </div>
        </div>
        
        <div class="main-content">
            <div class="header">
                <div>
                    <h1 class="domain-title">{domain}</h1>
                    <p class="scan-info">Scan conducted on {scan_time}</p>
                </div>
            </div>
            
            <div class="dashboard">
                <div class="dashboard-card">
                    <h2>Total Subdomains</h2>
                    <div class="value">{total_subdomains}</div>
                </div>
                <div class="dashboard-card">
                    <h2>Average Risk Score</h2>
                    <div class="value">{avg_score:.1f}</div>
                </div>
                <div class="dashboard-card">
                    <h2>High Risk Subdomains</h2>
                    <div class="value">{high_risk}</div>
                </div>
            </div>
            
            <div class="card">
                <h2>Subdomain Risk Analysis</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Subdomain</th>
                            <th>Risk Score</th>
                            <th>Risk Level</th>
                            <th>Reason</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
            
            <button class="collapsible">Raw JSON Data <span>+</span></button>
            <div class="content">
                <pre id="jsonData">{json_data}</pre>
            </div>
            
            <div class="footer">
                <p>Generated by SmartSubAI - AI-enhanced subdomain enumeration and filtering tool</p>
                <p>© {current_year} - SmartSubAI</p>
            </div>
        </div>
    </div>
    
    <script>
        // Collapsible sections
        var coll = document.getElementsByClassName("collapsible");
        var i;
        
        for (i = 0; i < coll.length; i++) {{
            coll[i].addEventListener("click", function() {{
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.maxHeight) {{
                    content.style.maxHeight = null;
                    this.getElementsByTagName('span')[0].innerHTML = '+';
                }} else {{
                    content.style.maxHeight = content.scrollHeight + "px";
                    this.getElementsByTagName('span')[0].innerHTML = '-';
                }}
            }});
        }}
    </script>
</body>
</html>
    """
    
    # Write the HTML to the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath 