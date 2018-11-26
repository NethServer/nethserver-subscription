Facter.add('firmware') do
    confine osfamily: 'RedHat'
    setcode do
        if File.directory?("/sys/firmware/efi")
            firmware = 'efi'
        else
            firmware = 'bios'
        end
        firmware
    end
end