# backup.rb

require 'date'
Facter.add('backup') do
    confine osfamily: 'RedHat'
    setcode do
        backup = {}
        backup_status = Facter::Core::Execution.exec('/sbin/e-smith/db backups getprop backup-data status')
        if backup_status == 'enabled'
            # Find most recent log file
            log_file = Dir.glob("/var/log/backup/backup-*").max_by {|f| File.mtime(f)}
            backup['last'] = {}
            backup['last']['type'] = Facter::Core::Execution.exec('/sbin/e-smith/db backups getprop backup-data VFSType')
            # If no log has been found, facter will catch the exception
            File.open(log_file, 'rb') do |f|
                while line = f.gets
                    if line =~ /^Backup started at (.*)$/
                        date = DateTime.parse(Regexp.last_match(1))
                        backup['last']['start'] = ''+date.to_time.to_i.to_s
                    end
                    if line =~ /^Backup ended at (.*)$/
                        date = DateTime.parse(Regexp.last_match(1))
                        backup['last']['end'] = date.to_time.to_i.to_s
                    end
                    if line =~ /^Backup status: (.*)$/
                        if Regexp.last_match(1) == 'SUCCESS'
                            backup['last']['ret_code'] = 0.to_s
                        else
                            backup['last']['ret_code'] = 1.to_s
                        end
                    end
                end
            end
        end
        backup
    end
end
