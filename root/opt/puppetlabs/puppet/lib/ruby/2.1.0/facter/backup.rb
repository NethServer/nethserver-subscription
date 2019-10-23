# backup.rb

require 'date'
Facter.add('backup') do
    confine osfamily: 'RedHat'
    setcode do
        backup = {}
        # Find most recent log file
        log_file = Dir.glob("/var/log/backup/backup-*").max_by {|f| File.mtime(f)}

        # Extract name
        parts = log_file.split('-')
        parts.delete('/var/log/backup/backup')
        parts.pop()
        name = parts.join('-')

        # Get backup status
        backup_status = Facter::Core::Execution.exec('/sbin/e-smith/db backups getprop '+name+' status')
        if backup_status == 'enabled'
            # Get props
            backup['last'] = {}
            type = Facter::Core::Execution.exec('/sbin/e-smith/db backups getprop '+name+' VFSType')
            engine = Facter::Core::Execution.exec('/sbin/e-smith/db backups gettype '+name)
            backup['last']['type'] = name +' ('+type+'|'+engine+')'

            # If no log has been found, facter will catch the exception
            File.open(log_file, 'rb') do |f|
                dateStart = ""
                while line = f.gets
                    if line =~ /^Backup started at (.*)$/
                        dateStart = DateTime.parse(Regexp.last_match(1))
                        backup['last']['start'] = ''+dateStart.to_time.to_i.to_s
                    end
                    if line =~ /^Backup ended at (.*)$/
                        dateEnd = DateTime.parse(Regexp.last_match(1))
                        backup['last']['end'] = dateEnd.to_time.to_i.to_s
                    end
                    if line =~ /^Backup status: (.*)$/
                        if Regexp.last_match(1) == 'SUCCESS'
                            backup['last']['ret_code'] = 0.to_s
                        else
                            # If failed return always 'end' prop, the same of start date
                            backup['last']['ret_code'] = 1.to_s
                            backup['last']['end'] = dateStart.to_time.to_i.to_s
                        end
                    end
                end
            end
        end
        backup
    end
end
