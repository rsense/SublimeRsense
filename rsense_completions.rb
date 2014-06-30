#!/usr/bin/env ruby

require 'optparse'
require 'json'
require 'net/http'

options = { command: "code_completion" }
OptionParser.new do |opts|
  opts.banner = "Usage: rsense start [options]"

  opts.on("--project PROJECT", "project path") do |project|
    options[:project] = project
  end

  opts.on("--filepath FILEPATH", "Filepath") do |filepath|
    options[:file] = filepath
  end

  opts.on("--text TEXT", "Text") do |text|
    options[:code] = text
  end

  opts.on("--location LOCATION", "Location") do |location|
    loc = location.split(':')
    row = loc.first
    col = loc.last
    options[:location] = { row: (row.to_i + 1), column: (col.to_i + 1) }
  end
end.parse!

jsondata = JSON.generate(options)

module Rsense
  class Request
    SOCKET_PATH = 'http://localhost'
    DEFAULT_PORT = 47367

    def self.req(jsondata)
      request = Net::HTTP::Post.new uri
      request.body = jsondata

      Net::HTTP.start(uri.host, uri.port) do |http|
        http.request request
      end
    end

    def self.uri
      uri = URI(SOCKET_PATH)
      uri.port = DEFAULT_PORT
      uri
    end
  end

  class Main
    def self.run(jsondata)
      req_body = request(jsondata).body
      completions_hash = JSON.parse(req_body)
      self.stringify(completions_hash)
    end

    def self.stringify(completions_hash)
      compls = completions_hash["completions"].map do |c|
        "#{c["name"]} #{c["qualified_name"]} #{c["base_name"]} #{c["kind"]}"
      end
      compls.join("\n")
    end

    def self.request(jsondata)
      Rsense::Request.req(jsondata)
    end
  end
end

compls = Rsense::Main.run(jsondata)

puts compls
