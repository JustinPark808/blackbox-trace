# Update/upgrade paackages and install auditd with plugins
echo '***apt-get is updating and upgrading all packages...'
sudo apt-get -qq update && apt-get -qq -y upgrade
echo '***apt-get is installing auditd and audispd-plugins...'
sudo apt-get -qq install -y auditd audispd-plugins

# Copy the defined rules into auditd's configuration directory
echo '***copying audit.rules into /etc/audit/rules.d/...'
sudo cp audit.rules /etc/audit/rules.d/

# Read the defined rules into auditd using auditctl
echo '***auditctl is reading rules from /etc/audit/rules.d/audit.rules...'
sudo auditctl -R /etc/audit/rules.d/audit.rules
