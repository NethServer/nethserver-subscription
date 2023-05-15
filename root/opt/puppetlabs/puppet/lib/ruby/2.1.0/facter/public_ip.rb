#
# public_ip
# Retrive public IP address
#

require "resolv"

Facter.add('public_ip') do
    confine osfamily: 'RedHat'
    setcode do
        public_ip = Facter::Core::Execution.exec("/usr/bin/curl -4 -m 5 ifconfig.co/")
        if !(public_ip =~ Resolv::IPv4::Regex)
            public_ip = ''
        end
        public_ip
    end
end
