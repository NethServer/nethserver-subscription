# backup.rb

Facter.add('backup') do
    confine osfamily: 'RedHat'
    setcode do
        backup = {}
        backup_status = Facter::Core::Execution.exec('/sbin/e-smith/db backups getprop backup-data status')
        if backup_status == 'enabled'
            # Find most recent log file
            log_file = Dir.glob("/var/log/backup/backup-backup-data-*").max_by {|f| File.mtime(f)}
            backup['last'] = {}
            backup['last']['type'] = Facter::Core::Execution.exec('/sbin/e-smith/db backups getprop backup-data VFSType')
            # If no log has been found, facter will catch the exception
            File.open(log_file, 'rb') do |f|
                while line = f.gets
                    backup['last']['start'] = Regexp.last_match(1) if line =~ /^StartTime\s(\d+)/
                    backup['last']['end'] = Regexp.last_match(1) if line =~ /^EndTime\s(\d+)/
                    backup['last']['ret_code'] = Regexp.last_match(1) if line =~ /^Errors\s(\d+)/
                end
            end
        end
        backup
    end
end
