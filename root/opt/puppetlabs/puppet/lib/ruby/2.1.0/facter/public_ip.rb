#
# public_ip
# Retrive public IP address
#

Facter.add('public_ip') do
    confine osfamily: 'RedHat'
    setcode do
        public_ip = Facter::Core::Execution.exec("/usr/bin/curl ifconfig.co/")
        public_ip
    end
end
