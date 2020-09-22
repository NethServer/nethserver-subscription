#
# Copyright (C) 2020 Nethesis S.r.l.
# http://www.nethesis.it - nethserver@nethesis.it
#
# This script is part of NethServer.
#
# NethServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# NethServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NethServer.  If not, see COPYING.
#

Facter.add('systemd') do
    confine osfamily: 'RedHat'
    setcode do
        systemd = {
            "restart" => {}
            "error" => ""
        }
        begin
            tmp = Facter::Core::Execution.execute("nice zgrep ', status=' $(find  /var/log/ -maxdepth 1 -name 'messages*' -newermt $(date -d '1 months ago' +@%s)) | awk '{print $6,$11}' | sort | uniq -c", :timeout => 60)
        rescue => error
            tmp = ""
            systemd["error"] = error.message
        end
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
