# Collaboration Network Analysis

This repository contains the final project report and implementation for the investigation of collaboration dynamics in a network of 51 research articles involving 106 collaborators. The project is divided into three primary tasks:

1. **Global-level Collaboration Network**
2. **Institutional-level Collaboration Network**
3. **Author-level Collaboration Network**

## Tools and Libraries Used

### Tools
- **Gephi**: A network visualization tool used to transform complex network topologies into intuitive and insightful visual representations.

### Python Libraries
- **NumPy (np)**: Provides multi-dimensional array objects and matrices for efficient mathematical, logical, and sorting operations.
- **NetworkX (nx)**: Main library for analyzing and visualizing complex networks and graphs.
- **Pandas (pd)**: Used for data manipulation and analysis.
- **Matplotlib (plt)**: A visualization library used to create histograms and other plots.

## Tasks Overview

### Task A: Global-level Collaboration Network

- **Data Extraction**: 
  Data was read from the `collaboration_network.xlsx` file using Pandas.
  ```python
  df0 = pd.read_excel('collaboration_network.xlsx', 'Co-author matrix', index_col=0)
  df1 = pd.read_excel('collaboration_network.xlsx', 'Paper list')
  df2 = pd.read_excel('collaboration_network.xlsx', 'People list')
  ```
- **Country Information**:
  Countries were extracted from the `Location of Institutional affiliation` column using lambda functions.
- **Adjacency Matrix**:
  A weighted adjacency matrix was created to capture collaborations between countries.
  ```python
  A_country = np.zeros((len(countries), len(countries)))
  for a, row in df0.iterrows():
      # Logic for constructing adjacency matrix
  ```

- **Visualizations**:
  - Heatmap representation of the adjacency matrix.
  - Degree distribution histogram.
  - Node centrality metrics (degree, betweenness, closeness).

#### Key Findings:
- The USA and China exhibit the highest centrality in international collaborations.
- Visualizations using Matplotlib and Gephi highlight collaboration dynamics and community structures.

### Task B: Institutional-level Collaboration Network

- **Data Extraction**:
  Institution names were extracted from the `Published affiliation` column.
  ```python
  def get_institution(s):
      return s.split(' (')[0].strip()
  ```
- **Adjacency Matrices**:
  Separate matrices were created for regional, national, and international collaborations.
  ```python
  A_reg = np.zeros((len(institutions), len(institutions)))
  A_nat = np.zeros((len(institutions), len(institutions)))
  A_int = np.zeros((len(institutions), len(institutions)))
  ```

#### Visualizations:
- Collaboration networks were plotted using both Python (NetworkX) and Gephi.

### Task C: Author-level Collaboration Network

- **Gender Analysis**:
  Gender distribution among lead and secondary authors was analyzed.
  - Pie charts were created to visualize the proportion of male and female authors.
  ```python
  genders1 = [df2[df2['author surname'] == surname]['gender'].values[0] for surname in df1['author1']]
  ```

#### Key Findings:
- A higher proportion of women were found among lead authors compared to secondary authors.

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install the required Python libraries:
   ```bash
   pip install numpy pandas matplotlib networkx
   ```
3. Run the scripts for each task to generate visualizations and analyses.

## Visualizations

- Heatmaps of adjacency matrices.
- Centrality graphs.
- Gender distribution pie charts.
- Gephi-based visual representations of collaboration networks.

## Conclusion

This project provides valuable insights into the dynamics of collaboration in research networks, highlighting key players, community structures, and trends at global, institutional, and author levels. The integration of Python libraries and Gephi significantly enhanced the analytical and visual representations.
