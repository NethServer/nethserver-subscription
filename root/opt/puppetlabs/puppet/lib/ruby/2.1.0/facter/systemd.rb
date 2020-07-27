# systemd.rb

Facter.add('systemd') do
    confine osfamily: 'RedHat'
    setcode do
        systemd = {
            "timestamp" => Time.now.to_i,
            "restart" => {}
        }
        tmp = Facter::Core::Execution.execute("zgrep ', status=' /var/log/messages* | awk '{print $6,$11}' | sort | uniq -c")
        tmp.split(/(\s+)?\n(\s+)?/).each do |record|
            fields = record.split(/\s+/)
            if fields.length() < 3 || !fields[2].start_with?('status=') then
              next
            end
            systemd["restart"][fields[1] + fields[2]] = Integer(fields[0])
        end
        systemd
    end
end
