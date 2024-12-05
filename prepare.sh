grep -v "^#" ms_data_dirty.csv|  # Remove comment lines
sed -e '/^$/d'| # Remove empty lines 
sed -e 's/,,/,/g'| # Remove extra commas  
cut -d ',' -f 1,2,4,5,6 > ms_data.csv # Extract columns

touch insurance.lst # create insurance list
echo -e "Basic \nPremium \nPlatinum" > insurance.lst

echo "Total number of visits: $(( $(wc -l < ms_data.csv) - 1 ))" # Count total number of visits exclude header

head -n 6 ms_data.csv

