# Update/upgrade paackages
echo '***apt-get is updating and upgrading all packages...'
sudo apt-get -qq update
sudo apt-get -qq -y upgrade

# Install auditd, audispd-plugins, and python3
echo '***apt-get is installing required packages...'
sudo apt-get -qq install -y auditd audispd-plugins python3

# Install required Python packages
echo '***pip3 is installing required Python packages...'
sudo pip3 -r ../trace/requirements.txt

# Copy the defined rules into auditd's configuration directory
echo '***copying audit.rules into /etc/audit/rules.d/...'
sudo cp audit.rules /etc/audit/rules.d/

# Read the defined rules into auditd using auditctl
echo '***auditctl is reading rules from /etc/audit/rules.d/audit.rules...'
sudo auditctl -R /etc/audit/rules.d/audit.rules
